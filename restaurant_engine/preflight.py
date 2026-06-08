from __future__ import annotations

import json
import math
import re
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .models import (
    ImageFile,
    PreflightReport,
    RenderParameterRecommendation,
    Shot,
    ShotPlan,
    TimingRecommendation,
    ValidationIssue,
)
from .validator import validate_project


ROLE_ORDER = ["intro", "interior", "dish_1", "dish_2", "dining", "extra"]
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}
MIN_CLIP_DURATION_SECONDS = 3
MAX_CLIP_DURATION_SECONDS = 6
NARRATION_SECONDS_BUFFER = 3
NARRATION_SAFE_CJK_CHARS_PER_SECOND = 4.0
NARRATION_FIELDS = [
    "narration",
    "voiceover",
    "script",
    "text",
    "description",
    "video_script",
    "user_request",
]


def run_preflight(project_path: str | Path) -> PreflightReport:
    project_file = Path(project_path).expanduser().resolve()
    issues: list[ValidationIssue] = []

    data = _read_project_data(project_file, issues)
    validation_report = validate_project(project_file)
    issues.extend(validation_report.issues)

    image_dir = Path(validation_report.image_dir) if validation_report.image_dir else project_file.parent
    image_files = _scan_image_files(image_dir, issues)

    narration_text, narration_field = _extract_narration_text(data)
    if not narration_text:
        issues.append(
            ValidationIssue(
                code="missing_narration_text",
                field="narration",
                severity="warning",
                message=(
                    "No narration text found. Supported fields: "
                    + ", ".join(NARRATION_FIELDS)
                ),
            )
        )
    elif narration_field == "user_request":
        issues.append(
            ValidationIssue(
                code="using_user_request_as_narration",
                field="user_request",
                severity="warning",
                message=(
                    "No dedicated narration field found; using user_request for "
                    "duration estimation."
                ),
            )
        )

    estimated_seconds = estimate_narration_duration(narration_text)
    target_duration_seconds = validation_report.target_duration_seconds
    recommended_duration = recommend_clip_duration(
        image_count=len(image_files),
        target_duration_seconds=target_duration_seconds,
    )
    narration_safe_seconds = get_narration_safe_seconds(target_duration_seconds)
    narration_max_cjk_chars = get_narration_max_cjk_chars(target_duration_seconds)
    _validate_narration_length(
        narration_text=narration_text,
        narration_max_cjk_chars=narration_max_cjk_chars,
        target_duration_seconds=target_duration_seconds,
        issues=issues,
    )
    shot_plan = build_shot_plan(image_files, recommended_duration)
    timing = validate_timing_coverage(
        image_count=len(image_files),
        clip_duration=recommended_duration,
        target_duration_seconds=target_duration_seconds,
        estimated_narration_seconds=estimated_seconds,
        narration_safe_seconds=narration_safe_seconds,
        narration_max_cjk_chars=narration_max_cjk_chars,
        issues=issues,
    )
    render_params = recommend_webui_params(timing)

    ok = not any(issue.severity == "error" for issue in issues)
    return PreflightReport(
        ok=ok,
        project_id=str(data.get("project_name") or project_file.stem),
        shot_plan=shot_plan,
        timing=timing,
        render_params=render_params,
        issues=issues,
    )


def build_shot_plan(
    image_files: list[ImageFile], recommended_duration: int
) -> ShotPlan:
    ordered_images = sorted(
        image_files,
        key=lambda image: (_role_sort_index(_detect_role(image.name)), image.name.lower()),
    )
    shots = [
        Shot(
            index=index,
            role=_detect_role(image.name),
            image_name=image.name,
            image_path=str(image.path),
            recommended_duration=recommended_duration,
        )
        for index, image in enumerate(ordered_images, start=1)
    ]
    present_roles = {_detect_role(image.name) for image in image_files}
    missing_roles = [role for role in ROLE_ORDER if role not in present_roles]
    return ShotPlan(
        shots=shots,
        total_image_duration=len(shots) * recommended_duration,
        missing_roles=missing_roles,
    )


def estimate_narration_duration(text: str) -> float:
    stripped_text = (text or "").strip()
    if not stripped_text:
        return 1.0

    cjk_chars = re.findall(r"[\u4e00-\u9fff]", stripped_text)
    english_words = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", stripped_text)

    # Rule of thumb only: Mandarin narration is estimated at 4.5 Chinese
    # characters per second, while English words use 150 words per minute.
    cjk_seconds = len(cjk_chars) / 4.5
    english_seconds = len(english_words) / 150 * 60
    estimated_seconds = cjk_seconds + english_seconds
    return max(1.0, round(estimated_seconds, 2))


def recommend_clip_duration(
    image_count: int,
    target_duration_seconds: int,
    min_seconds: int = MIN_CLIP_DURATION_SECONDS,
    max_seconds: int = MAX_CLIP_DURATION_SECONDS,
) -> int:
    if image_count <= 0:
        return min_seconds

    required_seconds = math.ceil(target_duration_seconds / image_count)
    return min(max(required_seconds, min_seconds), max_seconds)


def get_narration_safe_seconds(target_duration_seconds: int) -> int:
    return max(1, target_duration_seconds - NARRATION_SECONDS_BUFFER)


def get_narration_max_cjk_chars(target_duration_seconds: int) -> int:
    return math.floor(
        get_narration_safe_seconds(target_duration_seconds)
        * NARRATION_SAFE_CJK_CHARS_PER_SECOND
    )


def validate_timing_coverage(
    image_count: int,
    clip_duration: int,
    target_duration_seconds: int,
    estimated_narration_seconds: float,
    narration_safe_seconds: int,
    narration_max_cjk_chars: int,
    issues: list[ValidationIssue] | None = None,
) -> TimingRecommendation:
    total_image_duration = image_count * clip_duration
    will_loop = total_image_duration < max(
        target_duration_seconds, estimated_narration_seconds
    )

    if total_image_duration < target_duration_seconds and issues is not None:
        issues.append(
            ValidationIssue(
                code="image_duration_shorter_than_target_duration",
                field="video_clip_duration",
                severity="warning",
                message=(
                    f"Image coverage is {total_image_duration}s, shorter than "
                    f"target duration {target_duration_seconds}s. Increase images "
                    "or clip duration to avoid looping."
                ),
            )
        )

    if total_image_duration < estimated_narration_seconds and issues is not None:
        issues.append(
            ValidationIssue(
                code="image_duration_shorter_than_narration",
                field="video_clip_duration",
                severity="warning",
                message=(
                    f"Image coverage is {total_image_duration}s, shorter than "
                    f"estimated narration {estimated_narration_seconds}s. "
                    "WebUI may loop clips; increase target duration, add images, or "
                    "shorten narration."
                ),
            )
        )

    return TimingRecommendation(
        target_duration_seconds=target_duration_seconds,
        estimated_narration_seconds=estimated_narration_seconds,
        recommended_clip_duration=clip_duration,
        total_image_duration=total_image_duration,
        narration_safe_seconds=narration_safe_seconds,
        narration_max_cjk_chars=narration_max_cjk_chars,
        will_loop=will_loop,
    )


def recommend_webui_params(
    timing: TimingRecommendation,
) -> RenderParameterRecommendation:
    notes = [
        "Use Local file source with complete restaurant image set.",
        "Use Sequential concat mode; do not use random for restaurant shot order.",
        "Ensure image_count * video_clip_duration covers target and narration duration.",
    ]
    if timing.will_loop:
        notes.append(
            "Current recommendation may still loop; add images or shorten narration."
        )

    return RenderParameterRecommendation(
        video_concat_mode="sequential",
        video_clip_duration=timing.recommended_clip_duration,
        video_source="local",
        notes=notes,
    )


def preflight_report_to_dict(report: PreflightReport) -> dict[str, Any]:
    return asdict(report)


def write_preflight_report(report: PreflightReport, output_path: str | Path) -> None:
    output_file = Path(output_path).expanduser().resolve()
    output_file.write_text(
        json.dumps(preflight_report_to_dict(report), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _read_project_data(
    project_file: Path, issues: list[ValidationIssue]
) -> dict[str, Any]:
    if not project_file.exists():
        issues.append(
            ValidationIssue(
                code="project_json_missing",
                field="project",
                message=f"project.json does not exist: {project_file}",
            )
        )
        return {}

    try:
        data = json.loads(project_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        issues.append(
            ValidationIssue(
                code="project_json_invalid",
                field="project",
                message=f"project.json is not valid JSON: {exc}",
            )
        )
        return {}

    if not isinstance(data, dict):
        issues.append(
            ValidationIssue(
                code="project_json_not_object",
                field="project",
                message="project.json must contain a JSON object.",
            )
        )
        return {}

    return data


def _scan_image_files(
    image_dir: Path, issues: list[ValidationIssue]
) -> list[ImageFile]:
    if not image_dir.exists() or not image_dir.is_dir():
        return []

    images = [
        ImageFile(name=path.name, path=path.resolve(), suffix=path.suffix.lower())
        for path in image_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    ]
    if not images:
        issues.append(
            ValidationIssue(
                code="no_images_for_shot_plan",
                field="image_dir",
                message=f"No supported images found in image_dir: {image_dir}",
            )
        )
    return sorted(images, key=lambda image: image.name.lower())


def _extract_narration_text(data: dict[str, Any]) -> tuple[str, str | None]:
    for field_name in NARRATION_FIELDS:
        value = data.get(field_name)
        if isinstance(value, str) and value.strip():
            return value.strip(), field_name
    return "", None


def _validate_narration_length(
    narration_text: str,
    narration_max_cjk_chars: int,
    target_duration_seconds: int,
    issues: list[ValidationIssue],
) -> None:
    cjk_count = len(re.findall(r"[\u4e00-\u9fff]", narration_text or ""))
    if cjk_count > narration_max_cjk_chars:
        issues.append(
            ValidationIssue(
                code="narration_too_long_for_target_duration",
                field="narration",
                severity="warning",
                message=(
                    f"Narration has {cjk_count} Chinese characters, exceeding "
                    f"the safe limit {narration_max_cjk_chars} for "
                    f"{target_duration_seconds}s target duration."
                ),
            )
        )


def _detect_role(file_name: str) -> str:
    lower_name = file_name.lower()
    if "dish_1" in lower_name:
        return "dish_1"
    if "dish_2" in lower_name:
        return "dish_2"
    if "interior" in lower_name:
        return "interior"
    if "dining" in lower_name or "gathering" in lower_name:
        return "dining"
    if "extra" in lower_name:
        return "extra"
    if "intro" in lower_name or "storefront" in lower_name:
        return "intro"
    if "dish" in lower_name:
        return "dish"
    return "other"


def _role_sort_index(role: str) -> int:
    try:
        return ROLE_ORDER.index(role)
    except ValueError:
        return len(ROLE_ORDER)
