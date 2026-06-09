from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

from .models import (
    CoverPlan,
    CoverRenderReport,
    CoverRenderWarning,
)


COVER_RENDER_VERSION = "cover-render-v1"
COVER_RENDERER_NAME = "local_pillow"
COVER_IMAGE_FILE_NAME = "cover_image.png"
COVER_OUTPUT_FORMAT = "png"
COVER_OUTPUT_WIDTH = 1080
COVER_OUTPUT_HEIGHT = 1920

FONT_CANDIDATES = (
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
)


def render_cover_image(
    cover_plan: CoverPlan,
    output_dir: str | Path,
    source_cover_plan_path: str | Path | None = None,
    known_image_paths: list[str] | None = None,
) -> CoverRenderReport:
    """Render one local PNG cover image from the selected cover plan."""
    output_path = Path(output_dir).expanduser().resolve() / COVER_IMAGE_FILE_NAME
    warnings: list[CoverRenderWarning] = []

    validation_report = validate_cover_render_inputs(
        cover_plan=cover_plan,
        source_cover_plan_path=source_cover_plan_path,
        known_image_paths=known_image_paths,
    )
    if validation_report is not None:
        return validation_report

    try:
        from PIL import Image, ImageDraw, ImageFont, ImageOps
    except Exception as exc:
        return failed_cover_render_report(
            cover_plan=cover_plan,
            source_cover_plan_path=source_cover_plan_path,
            code="PIL_UNAVAILABLE",
            message=(
                "PIL/Pillow is not available in the current Python runtime; "
                f"cover rendering was skipped: {exc!r}"
            ),
        )

    source_image_path = resolve_source_image_path(
        cover_plan.selected_assets.primary_image_path,
        source_cover_plan_path=source_cover_plan_path,
        output_dir=output_dir,
    )
    title_text = get_cover_title_text(cover_plan)

    try:
        with Image.open(source_image_path) as image:
            base = ImageOps.exif_transpose(image).convert("RGB")
            canvas = center_crop_resize(
                base,
                width=COVER_OUTPUT_WIDTH,
                height=COVER_OUTPUT_HEIGHT,
            )
    except Exception as exc:
        return failed_cover_render_report(
            cover_plan=cover_plan,
            source_cover_plan_path=source_cover_plan_path,
            code="SOURCE_IMAGE_OPEN_FAILED",
            message=f"Failed to open selected cover source image: {exc!r}",
        )

    font, used_font, font_warning = load_cover_font(ImageFont)
    if font_warning is not None:
        warnings.append(font_warning)

    rendered = draw_cover_title(
        image=canvas,
        title_text=title_text,
        font=font,
        image_draw_module=ImageDraw,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rendered.save(output_path, format="PNG")

    return CoverRenderReport(
        version=COVER_RENDER_VERSION,
        renderer=COVER_RENDERER_NAME,
        external_api_called=False,
        render_status="rendered",
        cover_image_path=str(output_path),
        output_format=COVER_OUTPUT_FORMAT,
        output_width=COVER_OUTPUT_WIDTH,
        output_height=COVER_OUTPUT_HEIGHT,
        source_cover_plan_path=(
            str(Path(source_cover_plan_path).expanduser().resolve())
            if source_cover_plan_path is not None
            else None
        ),
        source_image_id=cover_plan.selected_assets.primary_image_id,
        source_image_path=str(source_image_path),
        title_text=title_text,
        title_source="selected_title",
        used_font=used_font,
        warnings=warnings,
        blocking=False,
    )


def validate_cover_render_inputs(
    cover_plan: CoverPlan,
    source_cover_plan_path: str | Path | None = None,
    known_image_paths: list[str] | None = None,
) -> CoverRenderReport | None:
    selected_title = cover_plan.selected_title
    cover_copy = cover_plan.cover_copy
    selected_assets = cover_plan.selected_assets

    if selected_title is None or not str(selected_title.text or "").strip():
        return failed_cover_render_report(
            cover_plan=cover_plan,
            source_cover_plan_path=source_cover_plan_path,
            code="TITLE_MISSING",
            message="cover_plan.selected_title.text is required for cover rendering.",
        )

    if cover_copy is None or not str(cover_copy.title or "").strip():
        return failed_cover_render_report(
            cover_plan=cover_plan,
            source_cover_plan_path=source_cover_plan_path,
            code="TITLE_MISSING",
            message="cover_plan.cover_copy.title is required for cover rendering.",
        )

    if str(cover_copy.title).strip() != str(selected_title.text).strip():
        return failed_cover_render_report(
            cover_plan=cover_plan,
            source_cover_plan_path=source_cover_plan_path,
            code="TITLE_MISMATCH",
            message=(
                "cover_plan.cover_copy.title must match "
                "cover_plan.selected_title.text before rendering."
            ),
        )

    if selected_assets is None or selected_assets.primary_image_id is None:
        return failed_cover_render_report(
            cover_plan=cover_plan,
            source_cover_plan_path=source_cover_plan_path,
            code="SOURCE_IMAGE_MISSING",
            message="cover_plan.selected_assets.primary_image_id is required.",
        )

    if not str(selected_assets.primary_image_path or "").strip():
        return failed_cover_render_report(
            cover_plan=cover_plan,
            source_cover_plan_path=source_cover_plan_path,
            code="SOURCE_IMAGE_MISSING",
            message="cover_plan.selected_assets.primary_image_path is required.",
        )

    source_image_path = resolve_source_image_path(
        selected_assets.primary_image_path,
        source_cover_plan_path=source_cover_plan_path,
        output_dir=None,
    )
    if not source_image_path.exists():
        return failed_cover_render_report(
            cover_plan=cover_plan,
            source_cover_plan_path=source_cover_plan_path,
            code="SOURCE_IMAGE_NOT_FOUND",
            message=f"Selected cover source image does not exist: {source_image_path}",
        )

    if known_image_paths:
        known_paths = {
            Path(path).expanduser().resolve()
            for path in known_image_paths
            if str(path or "").strip()
        }
        if source_image_path not in known_paths:
            return failed_cover_render_report(
                cover_plan=cover_plan,
                source_cover_plan_path=source_cover_plan_path,
                code="SOURCE_IMAGE_NOT_IN_CONTRACT",
                message=(
                    "Selected cover source image is not present in the "
                    "image_understanding contract."
                ),
            )

    return None


def failed_cover_render_report(
    cover_plan: CoverPlan,
    source_cover_plan_path: str | Path | None,
    code: str,
    message: str,
) -> CoverRenderReport:
    selected_assets = cover_plan.selected_assets
    source_image_path = (
        selected_assets.primary_image_path
        if selected_assets is not None
        else None
    )
    return CoverRenderReport(
        version=COVER_RENDER_VERSION,
        renderer=COVER_RENDERER_NAME,
        external_api_called=False,
        render_status="failed",
        cover_image_path=None,
        output_format=COVER_OUTPUT_FORMAT,
        output_width=0,
        output_height=0,
        source_cover_plan_path=(
            str(Path(source_cover_plan_path).expanduser().resolve())
            if source_cover_plan_path is not None
            else None
        ),
        source_image_id=(
            selected_assets.primary_image_id
            if selected_assets is not None
            else None
        ),
        source_image_path=source_image_path,
        title_text=get_cover_title_text(cover_plan),
        title_source="selected_title",
        used_font="none",
        warnings=[
            CoverRenderWarning(
                code=code,
                severity="error",
                message=message,
            )
        ],
        blocking=True,
    )


def resolve_source_image_path(
    raw_path: str | None,
    source_cover_plan_path: str | Path | None,
    output_dir: str | Path | None,
) -> Path:
    path = Path(str(raw_path or "")).expanduser()
    if path.is_absolute():
        return path.resolve()

    if source_cover_plan_path is not None:
        cover_plan_file = Path(source_cover_plan_path).expanduser().resolve()
        project_root = cover_plan_file.parent.parent
        candidate = (project_root / path).resolve()
        if candidate.exists():
            return candidate

    if output_dir is not None:
        candidate = (Path(output_dir).expanduser().resolve() / path).resolve()
        if candidate.exists():
            return candidate

    return path.resolve()


def get_cover_title_text(cover_plan: CoverPlan) -> str:
    if cover_plan.selected_title is not None:
        text = str(cover_plan.selected_title.text or "").strip()
        if text:
            return text
    if cover_plan.cover_copy is not None:
        return str(cover_plan.cover_copy.title or "").strip()
    return ""


def center_crop_resize(image, width: int, height: int):
    source_width, source_height = image.size
    target_ratio = width / height
    source_ratio = source_width / source_height

    if source_ratio > target_ratio:
        crop_width = int(source_height * target_ratio)
        left = (source_width - crop_width) // 2
        crop_box = (left, 0, left + crop_width, source_height)
    else:
        crop_height = int(source_width / target_ratio)
        top = (source_height - crop_height) // 2
        crop_box = (0, top, source_width, top + crop_height)

    return image.crop(crop_box).resize((width, height))


def load_cover_font(image_font_module):
    for font_path in FONT_CANDIDATES:
        path = Path(font_path)
        if not path.exists():
            continue
        try:
            return (
                image_font_module.truetype(str(path), size=92),
                path.name,
                None,
            )
        except Exception:
            continue

    return (
        image_font_module.load_default(),
        "PIL default font",
        CoverRenderWarning(
            code="FONT_FALLBACK_USED",
            severity="warning",
            message=(
                "No preferred system Chinese font was available; used PIL "
                "default font for cover title rendering."
            ),
        ),
    )


def draw_cover_title(image, title_text: str, font, image_draw_module):
    rendered = image.convert("RGBA")
    overlay = image_draw_module.Draw(rendered, "RGBA")
    width, height = rendered.size

    overlay.rectangle((0, 0, width, height), fill=(0, 0, 0, 60))
    panel_top = int(height * 0.12)
    panel_bottom = int(height * 0.40)
    overlay.rectangle((0, panel_top, width, panel_bottom), fill=(0, 0, 0, 130))

    lines = wrap_text_to_width(
        draw=overlay,
        text=title_text,
        font=font,
        max_width=int(width * 0.78),
    )
    line_metrics = [overlay.textbbox((0, 0), line, font=font) for line in lines]
    line_heights = [box[3] - box[1] for box in line_metrics]
    total_height = sum(line_heights) + max(0, len(lines) - 1) * 18
    y = panel_top + (panel_bottom - panel_top - total_height) // 2

    for line, box, line_height in zip(lines, line_metrics, line_heights):
        line_width = box[2] - box[0]
        x = (width - line_width) // 2
        overlay.text((x + 3, y + 3), line, font=font, fill=(0, 0, 0, 190))
        overlay.text((x, y), line, font=font, fill=(255, 255, 255, 255))
        y += line_height + 18

    return rendered.convert("RGB")


def wrap_text_to_width(draw, text: str, font, max_width: int) -> list[str]:
    text = str(text or "").strip()
    if not text:
        return [""]

    lines: list[str] = []
    current = ""
    for char in text:
        candidate = current + char
        bbox = draw.textbbox((0, 0), candidate, font=font)
        if bbox[2] - bbox[0] <= max_width or not current:
            current = candidate
            continue
        lines.append(current)
        current = char
    if current:
        lines.append(current)
    return lines[:3]


def cover_render_report_to_dict(report: CoverRenderReport) -> dict[str, Any]:
    return asdict(report)
