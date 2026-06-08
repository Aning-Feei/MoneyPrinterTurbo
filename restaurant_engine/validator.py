from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .models import ImageFile, ProjectConfig, ValidationIssue, ValidationReport


REQUIRED_FIELDS = [
    "project_name",
    "user_request",
    "selected_title",
    "aspect_ratio",
    "voice_type",
    "voice_enabled",
    "subtitle_enabled",
    "bgm_type",
    "video_style",
    "image_dir",
]

ALLOWED_ASPECT_RATIOS = {"9:16", "16:9"}
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}
FORBIDDEN_NAME_HINTS = [
    "qrcode",
    "qr",
    "phone",
    "tel",
    "address",
    "menu",
    "price",
    "contact",
    "wechat",
    "wx",
]


def validate_project(project_path: str | Path) -> ValidationReport:
    project_file = Path(project_path).expanduser().resolve()
    project_root = project_file.parent
    issues: list[ValidationIssue] = []

    data = _read_project_json(project_file, issues)
    _validate_required_fields(data, issues)

    config = _build_config(project_file, project_root, data)
    if config.aspect_ratio and config.aspect_ratio not in ALLOWED_ASPECT_RATIOS:
        issues.append(
            ValidationIssue(
                code="invalid_aspect_ratio",
                field="aspect_ratio",
                message='aspect_ratio must be "9:16" or "16:9".',
            )
        )

    image_dir_path = (project_root / config.image_dir).resolve() if config.image_dir else project_root
    image_files = _scan_images(image_dir_path, issues)
    category_checks = _check_categories(image_files)
    _validate_image_count(image_files, issues)
    _validate_categories(category_checks, issues)
    _validate_forbidden_name_hints(image_files, issues)

    report = ValidationReport(
        project_path=str(project_file),
        project_name=config.project_name,
        image_dir=str(image_dir_path),
        image_count=len(image_files),
        image_files=[image.name for image in image_files],
        category_checks=category_checks,
        issues=issues,
        passed=not issues,
    )
    return report


def report_to_dict(report: ValidationReport) -> dict[str, Any]:
    return asdict(report)


def write_report(report: ValidationReport, output_path: str | Path) -> None:
    output_file = Path(output_path).expanduser().resolve()
    output_file.write_text(
        json.dumps(report_to_dict(report), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _read_project_json(project_file: Path, issues: list[ValidationIssue]) -> dict[str, Any]:
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
        with project_file.open("r", encoding="utf-8") as file:
            data = json.load(file)
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


def _validate_required_fields(data: dict[str, Any], issues: list[ValidationIssue]) -> None:
    for field_name in REQUIRED_FIELDS:
        if field_name not in data:
            issues.append(
                ValidationIssue(
                    code="missing_required_field",
                    field=field_name,
                    message=f"Missing required field: {field_name}",
                )
            )


def _build_config(project_file: Path, project_root: Path, data: dict[str, Any]) -> ProjectConfig:
    return ProjectConfig(
        project_path=project_file,
        project_root=project_root,
        project_name=str(data.get("project_name", "")),
        user_request=str(data.get("user_request", "")),
        selected_title=str(data.get("selected_title", "")),
        aspect_ratio=str(data.get("aspect_ratio", "")),
        voice_type=str(data.get("voice_type", "")),
        voice_enabled=bool(data.get("voice_enabled", False)),
        subtitle_enabled=bool(data.get("subtitle_enabled", False)),
        bgm_type=str(data.get("bgm_type", "")),
        video_style=str(data.get("video_style", "")),
        image_dir=str(data.get("image_dir", "")),
        raw=data,
    )


def _scan_images(image_dir: Path, issues: list[ValidationIssue]) -> list[ImageFile]:
    if not image_dir.exists():
        issues.append(
            ValidationIssue(
                code="image_dir_missing",
                field="image_dir",
                message=f"image_dir does not exist: {image_dir}",
            )
        )
        return []

    if not image_dir.is_dir():
        issues.append(
            ValidationIssue(
                code="image_dir_not_directory",
                field="image_dir",
                message=f"image_dir is not a directory: {image_dir}",
            )
        )
        return []

    images = [
        ImageFile(name=path.name, path=path, suffix=path.suffix.lower())
        for path in image_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    ]
    return sorted(images, key=lambda image: image.name.lower())


def _validate_image_count(image_files: list[ImageFile], issues: list[ValidationIssue]) -> None:
    if len(image_files) < 6:
        issues.append(
            ValidationIssue(
                code="too_few_images",
                field="image_dir",
                message=f"At least 6 images are required; found {len(image_files)}.",
            )
        )

    if len(image_files) > 12:
        issues.append(
            ValidationIssue(
                code="too_many_images",
                field="image_dir",
                message=f"At most 12 images are allowed; found {len(image_files)}.",
            )
        )


def _check_categories(image_files: list[ImageFile]) -> dict[str, bool]:
    names = [image.name.lower() for image in image_files]
    return {
        "intro_or_storefront_or_dish": any(
            "intro" in name or "storefront" in name or "dish" in name for name in names
        ),
        "interior": any("interior" in name for name in names),
        "dish_1": any("dish_1" in name for name in names),
        "dish_2": any("dish_2" in name for name in names),
        "dining_or_gathering": any("dining" in name or "gathering" in name for name in names),
        "extra": any("extra" in name for name in names),
    }


def _validate_categories(
    category_checks: dict[str, bool], issues: list[ValidationIssue]
) -> None:
    labels = {
        "intro_or_storefront_or_dish": "intro/storefront/dish image",
        "interior": "interior image",
        "dish_1": "dish_1 image",
        "dish_2": "dish_2 image",
        "dining_or_gathering": "dining/gathering image",
        "extra": "extra image",
    }

    for category, passed in category_checks.items():
        if not passed:
            issues.append(
                ValidationIssue(
                    code="missing_image_category",
                    field="image_dir",
                    message=f"Missing required image category: {labels[category]}",
                )
            )


def _validate_forbidden_name_hints(
    image_files: list[ImageFile], issues: list[ValidationIssue]
) -> None:
    for image in image_files:
        lower_name = image.name.lower()
        matched_hints = [hint for hint in FORBIDDEN_NAME_HINTS if hint in lower_name]
        if matched_hints:
            issues.append(
                ValidationIssue(
                    code="forbidden_content_name_risk",
                    file_name=image.name,
                    message=(
                        "Image filename contains forbidden-content hint(s): "
                        + ", ".join(matched_hints)
                    ),
                )
            )
