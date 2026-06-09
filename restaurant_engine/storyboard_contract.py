from __future__ import annotations

from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

from .models import (
    ImageFile,
    Storyboard,
    StoryboardContractIssue,
    StoryboardContractReport,
)


REQUIRED_SCENE_FIELDS = (
    "index",
    "role",
    "image_name",
    "image_path",
    "duration_seconds",
)
MOCK_TEXT_MARKERS = (
    "Mock narration",
    "mock storyboard only",
)


def validate_storyboard_contract(
    storyboard: Storyboard | dict[str, Any],
    image_files: list[ImageFile | Path],
    target_duration_seconds: int,
    planner: str = "mock",
) -> StoryboardContractReport:
    storyboard_data = _to_dict(storyboard)
    expected_image_order = [_image_file_name(image) for image in image_files]
    scenes = storyboard_data.get("scenes")

    errors: list[StoryboardContractIssue] = []
    warnings: list[StoryboardContractIssue] = []
    actual_image_order: list[str] = []
    duration_sum = 0

    if not storyboard_data.get("project_id"):
        errors.append(_error("missing_project_id", "storyboard.project_id is required."))
    if not storyboard_data.get("version"):
        errors.append(_error("missing_version", "storyboard.version is required."))

    if not isinstance(scenes, list):
        errors.append(_error("missing_scenes", "storyboard.scenes must be a list."))
        return StoryboardContractReport(
            passed=False,
            errors=errors,
            warnings=warnings,
            scene_count=0,
            image_count=len(expected_image_order),
            target_duration_seconds=target_duration_seconds,
            duration_sum=0,
            expected_image_order=expected_image_order,
            actual_image_order=[],
        )

    actual_image_order = [
        str(scene.get("image_name") or "") if isinstance(scene, dict) else ""
        for scene in scenes
    ]
    if len(scenes) != len(expected_image_order):
        errors.append(
            _error(
                "scene_count_mismatch",
                (
                    f"storyboard has {len(scenes)} scenes, "
                    f"expected {len(expected_image_order)} images."
                ),
            )
        )

    if actual_image_order != expected_image_order:
        errors.append(
            _error(
                "scene_order_mismatch",
                "scene image_name order must match sorted image file order.",
            )
        )

    for expected_index, scene in enumerate(scenes, start=1):
        if not isinstance(scene, dict):
            errors.append(
                _error(
                    "invalid_scene",
                    f"scene {expected_index} must be a JSON object.",
                )
            )
            continue

        _validate_scene_fields(scene, expected_index, errors)
        _validate_scene_index(scene, expected_index, errors)
        _validate_scene_image(scene, expected_index, expected_image_order, errors)
        duration_sum += _validate_scene_duration(scene, expected_index, errors)
        _validate_scene_narration(scene, expected_index, planner, errors, warnings)

    total_duration = _coerce_int(storyboard_data.get("total_duration_seconds"))
    if duration_sum != target_duration_seconds:
        errors.append(
            _error(
                "duration_sum_mismatch",
                (
                    f"scene duration sum is {duration_sum}, "
                    f"expected {target_duration_seconds}."
                ),
            )
        )
    if total_duration != target_duration_seconds:
        errors.append(
            _error(
                "total_duration_mismatch",
                (
                    f"storyboard.total_duration_seconds is {total_duration}, "
                    f"expected {target_duration_seconds}."
                ),
            )
        )

    return StoryboardContractReport(
        passed=not errors,
        errors=errors,
        warnings=warnings,
        scene_count=len(scenes),
        image_count=len(expected_image_order),
        target_duration_seconds=target_duration_seconds,
        duration_sum=duration_sum,
        expected_image_order=expected_image_order,
        actual_image_order=actual_image_order,
    )


def storyboard_contract_report_to_dict(
    report: StoryboardContractReport,
) -> dict[str, Any]:
    return asdict(report)


def _validate_scene_fields(
    scene: dict[str, Any],
    expected_index: int,
    errors: list[StoryboardContractIssue],
) -> None:
    for field in REQUIRED_SCENE_FIELDS:
        if field not in scene:
            errors.append(
                _error(
                    "missing_scene_field",
                    f"scene {expected_index} missing required field: {field}.",
                )
            )

    if "narration" not in scene and "mock_narration" not in scene:
        errors.append(
            _error(
                "missing_scene_field",
                f"scene {expected_index} missing required narration field.",
            )
        )


def _validate_scene_index(
    scene: dict[str, Any],
    expected_index: int,
    errors: list[StoryboardContractIssue],
) -> None:
    if _coerce_int(scene.get("index")) != expected_index:
        errors.append(
            _error(
                "invalid_scene_index",
                f"scene index must be {expected_index}.",
            )
        )


def _validate_scene_image(
    scene: dict[str, Any],
    expected_index: int,
    expected_image_order: list[str],
    errors: list[StoryboardContractIssue],
) -> None:
    image_name = str(scene.get("image_name") or "")
    if expected_index <= len(expected_image_order):
        expected_image_name = expected_image_order[expected_index - 1]
        if image_name != expected_image_name:
            errors.append(
                _error(
                    "scene_order_mismatch",
                    (
                        f"scene {expected_index} image_name is {image_name!r}, "
                        f"expected {expected_image_name!r}."
                    ),
                )
            )

    image_path = scene.get("image_path")
    if not isinstance(image_path, str) or not image_path:
        errors.append(
            _error(
                "invalid_image_path",
                f"scene {expected_index} image_path must be a non-empty string.",
            )
        )
        return

    if Path(image_path).name != image_name:
        errors.append(
            _error(
                "image_path_mismatch",
                f"scene {expected_index} image_path file name must match image_name.",
            )
        )


def _validate_scene_duration(
    scene: dict[str, Any],
    expected_index: int,
    errors: list[StoryboardContractIssue],
) -> int:
    duration = _coerce_int(scene.get("duration_seconds"))
    if duration <= 0:
        errors.append(
            _error(
                "invalid_duration",
                f"scene {expected_index} duration_seconds must be a positive integer.",
            )
        )
        return 0
    return duration


def _validate_scene_narration(
    scene: dict[str, Any],
    expected_index: int,
    planner: str,
    errors: list[StoryboardContractIssue],
    warnings: list[StoryboardContractIssue],
) -> None:
    narration = str(scene.get("narration") or scene.get("mock_narration") or "")
    if not narration.strip():
        errors.append(
            _error(
                "empty_narration",
                f"scene {expected_index} narration must not be empty.",
            )
        )
        return

    if any(marker in narration for marker in MOCK_TEXT_MARKERS):
        issue = StoryboardContractIssue(
            level="warning" if planner == "mock" else "error",
            code=(
                "mock_text_in_mock_storyboard"
                if planner == "mock"
                else "mock_text_in_deepseek_storyboard"
            ),
            message=f"scene {expected_index} narration contains mock placeholder text.",
        )
        if planner == "mock":
            warnings.append(issue)
        else:
            errors.append(issue)


def _to_dict(storyboard: Storyboard | dict[str, Any]) -> dict[str, Any]:
    if isinstance(storyboard, dict):
        return storyboard
    if is_dataclass(storyboard):
        return asdict(storyboard)
    raise TypeError("storyboard must be a Storyboard dataclass or dict.")


def _image_file_name(image: ImageFile | Path) -> str:
    if isinstance(image, ImageFile):
        return image.name
    return Path(image).name


def _coerce_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _error(code: str, message: str) -> StoryboardContractIssue:
    return StoryboardContractIssue(level="error", code=code, message=message)
