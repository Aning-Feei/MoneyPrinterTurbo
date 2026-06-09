from __future__ import annotations

import json
import re
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .models import (
    ImageFile,
    PipelineReport,
    PipelineStep,
)
from .deepseek_client import DeepSeekClient
from .storyboard_planner import (
    SUPPORTED_PLANNERS,
    build_deepseek_storyboard,
    build_mock_storyboard,
    get_project_id,
    get_target_duration_seconds,
)
from .validator import IMAGE_SUFFIXES, report_to_dict, validate_project


STORYBOARD_FILE_NAME = "storyboard.json"
PIPELINE_REPORT_FILE_NAME = "pipeline_report.json"


def run_pipeline(
    project_json_path: str | Path,
    planner: str = "mock",
    allow_external_api: bool = False,
) -> PipelineReport:
    """Run the stage-2 pipeline for a restaurant project."""
    project_file = Path(project_json_path).expanduser().resolve()
    project_root = resolve_project_root(project_file)
    output_dir = project_root / "output"
    planner_name = normalize_planner(planner)

    project_config: dict[str, Any] = {}
    image_dir: Path | None = None
    image_files: list[ImageFile] = []
    storyboard_path: str | None = None
    validation_passed = False
    external_api_called = False
    issues: list[dict[str, Any]] = []
    steps: list[PipelineStep] = []

    if planner_name not in SUPPORTED_PLANNERS:
        issues.append(
            _pipeline_issue(
                "unsupported_planner",
                f"Unsupported planner: {planner_name}. Supported planners: mock, deepseek.",
            )
        )
        steps.append(
            PipelineStep(
                name="select_planner",
                status="failed",
                message=f"Unsupported planner: {planner_name}",
            )
        )
    else:
        steps.append(
            PipelineStep(
                name="select_planner",
                status="passed",
                message=f"Selected planner: {planner_name}",
            )
        )

    try:
        project_config = load_project_json(project_file)
        steps.append(
            PipelineStep(
                name="load_project_json",
                status="passed",
                message=f"Loaded project JSON: {project_file}",
            )
        )
    except Exception as exc:
        issues.append(_pipeline_issue("load_project_json_failed", str(exc)))
        steps.append(
            PipelineStep(
                name="load_project_json",
                status="failed",
                message=str(exc),
            )
        )

    try:
        validation_report = validate_project(project_file)
        validation_data = report_to_dict(validation_report)
        validation_passed = validation_report.passed
        issues.extend(validation_data.get("issues", []))
        steps.append(
            PipelineStep(
                name="validate_project",
                status="passed" if validation_report.passed else "failed",
                message=(
                    "Validation passed"
                    if validation_report.passed
                    else "Validation completed with errors"
                ),
            )
        )
    except Exception as exc:
        issues.append(_pipeline_issue("validate_project_failed", str(exc)))
        steps.append(
            PipelineStep(
                name="validate_project",
                status="failed",
                message=str(exc),
            )
        )

    try:
        image_dir = resolve_image_dir(project_config, project_file)
        steps.append(
            PipelineStep(
                name="resolve_image_dir",
                status="passed",
                message=f"Resolved image directory: {image_dir}",
            )
        )
    except Exception as exc:
        issues.append(_pipeline_issue("resolve_image_dir_failed", str(exc)))
        steps.append(
            PipelineStep(
                name="resolve_image_dir",
                status="failed",
                message=str(exc),
            )
        )

    try:
        if image_dir is None:
            raise ValueError("Image directory is not resolved.")
        image_files = scan_image_files(image_dir)
        steps.append(
            PipelineStep(
                name="scan_images",
                status="passed",
                message=f"Found {len(image_files)} local images.",
            )
        )
    except Exception as exc:
        issues.append(_pipeline_issue("scan_images_failed", str(exc)))
        steps.append(
            PipelineStep(
                name="scan_images",
                status="failed",
                message=str(exc),
            )
        )

    try:
        output_dir = create_output_dir(project_root)
        steps.append(
            PipelineStep(
                name="create_output_dir",
                status="passed",
                message=f"Created output directory: {output_dir}",
            )
        )
    except Exception as exc:
        issues.append(_pipeline_issue("create_output_dir_failed", str(exc)))
        steps.append(
            PipelineStep(
                name="create_output_dir",
                status="failed",
                message=str(exc),
            )
        )

    can_plan_storyboard = (
        validation_passed
        and image_dir is not None
        and bool(image_files)
        and planner_name in SUPPORTED_PLANNERS
        and not _has_failed_step(
            steps,
            {
                "select_planner",
                "load_project_json",
                "resolve_image_dir",
                "scan_images",
                "create_output_dir",
            },
        )
    )

    storyboard = None
    if can_plan_storyboard and planner_name == "deepseek" and not allow_external_api:
        issues.append(
            _pipeline_issue(
                "external_api_not_allowed",
                "DeepSeek planner requires allow_external_api=True.",
            )
        )
        steps.append(
            PipelineStep(
                name="plan_storyboard",
                status="failed",
                message="DeepSeek planner requires --allow-external-api.",
            )
        )
    elif can_plan_storyboard:
        try:
            if planner_name == "mock":
                storyboard = build_mock_storyboard(project_config, image_files)
            else:
                deepseek_client = DeepSeekClient()
                try:
                    storyboard = build_deepseek_storyboard(
                        project_config,
                        image_files,
                        client=deepseek_client,
                    )
                finally:
                    external_api_called = deepseek_client.external_api_called

            steps.append(
                PipelineStep(
                    name="plan_storyboard",
                    status="passed",
                    message=(
                        f"Built {planner_name} storyboard with "
                        f"{len(storyboard.scenes)} scenes."
                    ),
                )
            )
        except Exception as exc:
            issues.append(_pipeline_issue("plan_storyboard_failed", str(exc)))
            steps.append(
                PipelineStep(
                    name="plan_storyboard",
                    status="failed",
                    message=str(exc),
                )
            )
    else:
        steps.append(
            PipelineStep(
                name="plan_storyboard",
                status="skipped",
                message="Skipped because validation or image scanning did not pass.",
            )
        )

    if storyboard is not None:
        try:
            storyboard_file = write_storyboard(output_dir, storyboard)
            storyboard_path = str(storyboard_file)
            steps.append(
                PipelineStep(
                    name="write_storyboard",
                    status="passed",
                    message=f"Wrote storyboard: {storyboard_file}",
                )
            )
        except Exception as exc:
            issues.append(_pipeline_issue("write_storyboard_failed", str(exc)))
            steps.append(
                PipelineStep(
                    name="write_storyboard",
                    status="failed",
                    message=str(exc),
                )
            )
    else:
        steps.append(
            PipelineStep(
                name="write_storyboard",
                status="skipped",
                message="Skipped because no storyboard was built.",
            )
        )

    report = _build_report(
        project_config=project_config,
        project_file=project_file,
        image_dir=image_dir,
        output_dir=output_dir,
        image_count=len(image_files),
        storyboard_path=storyboard_path,
        validation_passed=validation_passed,
        planner=planner_name,
        external_api_allowed=allow_external_api,
        external_api_called=external_api_called,
        storyboard=storyboard,
        steps=steps,
        issues=issues,
    )

    report_path = output_dir / PIPELINE_REPORT_FILE_NAME
    try:
        steps.append(
            PipelineStep(
                name="write_pipeline_report",
                status="passed",
                message=f"Wrote pipeline report: {report_path}",
            )
        )
        report = _build_report(
            project_config=project_config,
            project_file=project_file,
            image_dir=image_dir,
            output_dir=output_dir,
            image_count=len(image_files),
            storyboard_path=storyboard_path,
            validation_passed=validation_passed,
            planner=planner_name,
            external_api_allowed=allow_external_api,
            external_api_called=external_api_called,
            storyboard=storyboard,
            steps=steps,
            issues=issues,
        )
        write_pipeline_report(output_dir, report)
    except Exception as exc:
        issues.append(_pipeline_issue("write_pipeline_report_failed", str(exc)))
        steps.append(
            PipelineStep(
                name="write_pipeline_report",
                status="failed",
                message=str(exc),
            )
        )
        report = _build_report(
            project_config=project_config,
            project_file=project_file,
            image_dir=image_dir,
            output_dir=output_dir,
            image_count=len(image_files),
            storyboard_path=storyboard_path,
            validation_passed=validation_passed,
            planner=planner_name,
            external_api_allowed=allow_external_api,
            external_api_called=external_api_called,
            storyboard=storyboard,
            steps=steps,
            issues=issues,
        )

    return report


def load_project_json(project_json_path: str | Path) -> dict[str, Any]:
    project_file = Path(project_json_path).expanduser().resolve()
    with project_file.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("project.json must contain a JSON object.")

    return data


def resolve_project_root(project_json_path: str | Path) -> Path:
    return Path(project_json_path).expanduser().resolve().parent


def resolve_image_dir(project_config: dict[str, Any], project_json_path: str | Path) -> Path:
    project_root = resolve_project_root(project_json_path)
    raw_image_dir = str(project_config.get("image_dir") or "")
    if not raw_image_dir:
        return project_root

    image_dir = Path(raw_image_dir).expanduser()
    if image_dir.is_absolute():
        return image_dir.resolve()
    return (project_root / image_dir).resolve()


def scan_image_files(image_dir: str | Path) -> list[ImageFile]:
    image_dir_path = Path(image_dir).expanduser().resolve()
    if not image_dir_path.exists():
        raise FileNotFoundError(f"image_dir does not exist: {image_dir_path}")
    if not image_dir_path.is_dir():
        raise NotADirectoryError(f"image_dir is not a directory: {image_dir_path}")

    images = [
        ImageFile(name=path.name, path=path, suffix=path.suffix.lower())
        for path in image_dir_path.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    ]
    return sorted(images, key=lambda image: _natural_sort_key(image.name))


def create_output_dir(project_root: str | Path) -> Path:
    output_dir = Path(project_root).expanduser().resolve() / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def write_storyboard(output_dir: str | Path, storyboard) -> Path:
    storyboard_path = Path(output_dir).expanduser().resolve() / STORYBOARD_FILE_NAME
    _write_json(storyboard_path, asdict(storyboard))
    return storyboard_path


def write_pipeline_report(output_dir: str | Path, report: PipelineReport) -> Path:
    report_path = Path(output_dir).expanduser().resolve() / PIPELINE_REPORT_FILE_NAME
    _write_json(report_path, pipeline_report_to_dict(report))
    return report_path


def pipeline_report_to_dict(report: PipelineReport) -> dict[str, Any]:
    return asdict(report)


def normalize_planner(planner: str) -> str:
    return str(planner or "mock").strip().lower()


def _build_report(
    project_config: dict[str, Any],
    project_file: Path,
    image_dir: Path | None,
    output_dir: Path,
    image_count: int,
    storyboard_path: str | None,
    validation_passed: bool,
    planner: str,
    external_api_allowed: bool,
    external_api_called: bool,
    storyboard,
    steps: list[PipelineStep],
    issues: list[dict[str, Any]],
) -> PipelineReport:
    ok = (
        validation_passed
        and storyboard_path is not None
        and not any(step.status == "failed" for step in steps)
    )
    return PipelineReport(
        ok=ok,
        project_id=get_project_id(project_config),
        project_json_path=str(project_file),
        image_dir=str(image_dir) if image_dir is not None else "",
        output_dir=str(output_dir),
        image_count=image_count,
        storyboard_path=storyboard_path,
        validation_passed=validation_passed,
        target_duration_seconds=get_target_duration_seconds(project_config),
        scene_count=len(storyboard.scenes) if storyboard is not None else 0,
        scene_durations=(
            [scene.duration_seconds for scene in storyboard.scenes]
            if storyboard is not None
            else []
        ),
        total_duration_seconds=(
            storyboard.total_duration_seconds if storyboard is not None else 0
        ),
        duration_normalized=storyboard is not None,
        planner=planner,
        external_api_allowed=external_api_allowed,
        external_api_called=external_api_called,
        steps=list(steps),
        issues=list(issues),
    )


def _write_json(output_path: Path, data: dict[str, Any]) -> None:
    output_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _pipeline_issue(code: str, message: str) -> dict[str, Any]:
    return {
        "code": code,
        "message": message,
        "severity": "error",
        "field": None,
        "file_name": None,
    }


def _has_failed_step(steps: list[PipelineStep], names: set[str]) -> bool:
    return any(step.name in names and step.status == "failed" for step in steps)


def _natural_sort_key(name: str) -> list[int | str]:
    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r"(\d+)", name)
    ]
