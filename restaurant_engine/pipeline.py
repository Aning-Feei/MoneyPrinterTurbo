from __future__ import annotations

import json
import re
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .models import (
    ImageFile,
    ImageUnderstandingReport,
    NarrationPlan,
    PipelineReport,
    PipelineStep,
)
from .image_understanding import (
    SUPPORTED_IMAGE_UNDERSTANDING_PROVIDERS,
    build_image_understanding,
    normalize_image_understanding_provider,
)
from .deepseek_client import DeepSeekClient
from .storyboard_planner import (
    SUPPORTED_PLANNERS,
    build_deepseek_storyboard,
    build_mock_storyboard,
    get_project_id,
    get_target_duration_seconds,
)
from .storyboard_contract import (
    validate_storyboard_contract,
    validate_storyboard_quality_contract,
)
from .narration_plan import (
    build_narration_plan,
    validate_tts_contract,
)
from .validator import IMAGE_SUFFIXES, report_to_dict, validate_project


STORYBOARD_FILE_NAME = "storyboard.json"
IMAGE_UNDERSTANDING_FILE_NAME = "image_understanding.json"
NARRATION_PLAN_FILE_NAME = "narration_plan.json"
PIPELINE_REPORT_FILE_NAME = "pipeline_report.json"


def run_pipeline(
    project_json_path: str | Path,
    planner: str = "mock",
    image_understanding_provider: str = "mock",
    allow_external_api: bool = False,
) -> PipelineReport:
    """Run the stage-2 pipeline for a restaurant project."""
    project_file = Path(project_json_path).expanduser().resolve()
    project_root = resolve_project_root(project_file)
    output_dir = project_root / "output"
    planner_name = normalize_planner(planner)
    image_provider_name = normalize_image_understanding_provider(
        image_understanding_provider
    )

    project_config: dict[str, Any] = {}
    image_dir: Path | None = None
    image_files: list[ImageFile] = []
    image_understanding: ImageUnderstandingReport | None = None
    image_understanding_path: str | None = None
    storyboard_path: str | None = None
    narration_plan_path: str | None = None
    validation_passed = False
    external_api_called = False
    storyboard_contract_report = None
    storyboard_quality_report = None
    narration_plan: NarrationPlan | None = None
    tts_contract_report = None
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

    if image_provider_name not in SUPPORTED_IMAGE_UNDERSTANDING_PROVIDERS:
        issues.append(
            _pipeline_issue(
                "unsupported_image_understanding_provider",
                (
                    "Unsupported image understanding provider: "
                    f"{image_provider_name}. Supported providers: "
                    f"{', '.join(SUPPORTED_IMAGE_UNDERSTANDING_PROVIDERS)}."
                ),
            )
        )
        steps.append(
            PipelineStep(
                name="select_image_understanding_provider",
                status="failed",
                message=(
                    "Unsupported image understanding provider: "
                    f"{image_provider_name}"
                ),
            )
        )
    else:
        steps.append(
            PipelineStep(
                name="select_image_understanding_provider",
                status="passed",
                message=f"Selected image understanding provider: {image_provider_name}",
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

    can_build_image_understanding = (
        validation_passed
        and image_dir is not None
        and not _has_failed_step(
            steps,
            {
                "load_project_json",
                "validate_project",
                "resolve_image_dir",
                "scan_images",
                "create_output_dir",
                "select_image_understanding_provider",
            },
        )
    )
    if image_provider_name == "vision" and not allow_external_api:
        issues.append(
            _pipeline_issue(
                "image_understanding_external_api_not_allowed",
                "Vision image understanding requires --allow-external-api.",
            )
        )
        steps.append(
            PipelineStep(
                name="build_image_understanding",
                status="failed",
                message="Vision image understanding requires --allow-external-api.",
            )
        )
        can_build_image_understanding = False

    if can_build_image_understanding:
        try:
            image_understanding = build_image_understanding(
                project_id=get_project_id(project_config),
                image_dir=image_dir,
                image_files=image_files,
                provider=image_provider_name,
                allow_external_api=allow_external_api,
            )
            if image_understanding.errors:
                issues.extend(
                    _image_understanding_errors_to_pipeline_issues(
                        image_understanding.errors
                    )
                )
                steps.append(
                    PipelineStep(
                        name="build_image_understanding",
                        status="failed",
                        message=(
                            "Image understanding failed with "
                            f"{len(image_understanding.errors)} errors."
                        ),
                    )
                )
            else:
                issues.extend(
                    _image_understanding_warnings_to_pipeline_issues(
                        image_understanding.warnings
                    )
                )
                steps.append(
                    PipelineStep(
                        name="build_image_understanding",
                        status="passed",
                        message=(
                            f"Built {image_provider_name} image understanding for "
                            f"{image_understanding.image_count} images."
                        ),
                    )
                )
        except Exception as exc:
            issues.append(_pipeline_issue("build_image_understanding_failed", str(exc)))
            steps.append(
                PipelineStep(
                    name="build_image_understanding",
                    status="failed",
                    message=str(exc),
                )
            )
    else:
        if not _has_failed_step(steps, {"build_image_understanding"}):
            steps.append(
                PipelineStep(
                    name="build_image_understanding",
                    status="skipped",
                    message=(
                        "Skipped because validation, image scanning, or provider "
                        "selection did not pass."
                    ),
                )
            )

    if image_understanding is not None:
        try:
            image_understanding_file = write_image_understanding(
                output_dir,
                image_understanding,
            )
            image_understanding_path = str(image_understanding_file)
            steps.append(
                PipelineStep(
                    name="write_image_understanding",
                    status="passed",
                    message=f"Wrote image understanding: {image_understanding_file}",
                )
            )
        except Exception as exc:
            issues.append(_pipeline_issue("write_image_understanding_failed", str(exc)))
            steps.append(
                PipelineStep(
                    name="write_image_understanding",
                    status="failed",
                    message=str(exc),
                )
            )
    else:
        steps.append(
            PipelineStep(
                name="write_image_understanding",
                status="skipped",
                message="Skipped because no image understanding was built.",
            )
        )

    can_plan_storyboard = can_plan_storyboard and not _has_failed_step(
        steps,
        {
            "select_image_understanding_provider",
            "build_image_understanding",
            "write_image_understanding",
        },
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
            storyboard_contract_report = validate_storyboard_contract(
                storyboard=storyboard,
                image_files=image_files,
                target_duration_seconds=get_target_duration_seconds(project_config),
                planner=planner_name,
            )
            if storyboard_contract_report.passed:
                steps.append(
                    PipelineStep(
                        name="validate_storyboard_contract",
                        status="passed",
                        message=(
                            "Storyboard contract passed with "
                            f"{len(storyboard_contract_report.warnings)} warnings."
                        ),
                    )
                )
            else:
                issues.extend(
                    _contract_issues_to_pipeline_issues(
                        storyboard_contract_report.errors
                    )
                )
                steps.append(
                    PipelineStep(
                        name="validate_storyboard_contract",
                        status="failed",
                        message=(
                            "Storyboard contract failed with "
                            f"{len(storyboard_contract_report.errors)} errors."
                        ),
                    )
                )
        except Exception as exc:
            issues.append(_pipeline_issue("storyboard_contract_failed", str(exc)))
            steps.append(
                PipelineStep(
                    name="validate_storyboard_contract",
                    status="failed",
                    message=str(exc),
                )
            )
    else:
        steps.append(
            PipelineStep(
                name="validate_storyboard_contract",
                status="skipped",
                message="Skipped because no storyboard was built.",
            )
        )

    if storyboard is not None:
        try:
            storyboard_quality_report = validate_storyboard_quality_contract(
                storyboard=storyboard,
                planner=planner_name,
            )
            if storyboard_quality_report.passed:
                steps.append(
                    PipelineStep(
                        name="validate_storyboard_quality",
                        status="passed",
                        message=(
                            "Storyboard quality contract passed with "
                            f"{len(storyboard_quality_report.warnings)} warnings."
                        ),
                    )
                )
            else:
                issues.extend(
                    _contract_issues_to_pipeline_issues(
                        storyboard_quality_report.errors
                    )
                )
                steps.append(
                    PipelineStep(
                        name="validate_storyboard_quality",
                        status="failed",
                        message=(
                            "Storyboard quality contract failed with "
                            f"{len(storyboard_quality_report.errors)} errors."
                        ),
                    )
                )
        except Exception as exc:
            issues.append(_pipeline_issue("storyboard_quality_failed", str(exc)))
            steps.append(
                PipelineStep(
                    name="validate_storyboard_quality",
                    status="failed",
                    message=str(exc),
                )
            )
    else:
        steps.append(
            PipelineStep(
                name="validate_storyboard_quality",
                status="skipped",
                message="Skipped because no storyboard was built.",
            )
        )

    can_build_narration_plan = (
        storyboard is not None
        and storyboard_contract_report is not None
        and storyboard_contract_report.passed
        and storyboard_quality_report is not None
        and storyboard_quality_report.passed
    )
    if can_build_narration_plan:
        try:
            narration_plan = build_narration_plan(storyboard)
            steps.append(
                PipelineStep(
                    name="build_narration_plan",
                    status="passed",
                    message=(
                        "Built narration plan with "
                        f"{len(narration_plan.lines)} lines."
                    ),
                )
            )
        except Exception as exc:
            issues.append(_pipeline_issue("build_narration_plan_failed", str(exc)))
            steps.append(
                PipelineStep(
                    name="build_narration_plan",
                    status="failed",
                    message=str(exc),
                )
            )
    else:
        steps.append(
            PipelineStep(
                name="build_narration_plan",
                status="skipped",
                message="Skipped because storyboard contracts did not pass.",
            )
        )

    if narration_plan is not None:
        try:
            tts_contract_report = validate_tts_contract(
                narration_plan=narration_plan,
                scene_count=len(storyboard.scenes) if storyboard is not None else 0,
            )
            if tts_contract_report.passed:
                steps.append(
                    PipelineStep(
                        name="validate_tts_contract",
                        status="passed",
                        message=(
                            "TTS contract passed with "
                            f"{len(tts_contract_report.warnings)} warnings."
                        ),
                    )
                )
            else:
                issues.extend(
                    _contract_issues_to_pipeline_issues(
                        tts_contract_report.errors
                    )
                )
                steps.append(
                    PipelineStep(
                        name="validate_tts_contract",
                        status="failed",
                        message=(
                            "TTS contract failed with "
                            f"{len(tts_contract_report.errors)} errors."
                        ),
                    )
                )
        except Exception as exc:
            issues.append(_pipeline_issue("tts_contract_failed", str(exc)))
            steps.append(
                PipelineStep(
                    name="validate_tts_contract",
                    status="failed",
                    message=str(exc),
                )
            )
    else:
        steps.append(
            PipelineStep(
                name="validate_tts_contract",
                status="skipped",
                message="Skipped because no narration plan was built.",
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

    if narration_plan is not None:
        try:
            narration_plan_file = write_narration_plan(output_dir, narration_plan)
            narration_plan_path = str(narration_plan_file)
            steps.append(
                PipelineStep(
                    name="write_narration_plan",
                    status="passed",
                    message=f"Wrote narration plan: {narration_plan_file}",
                )
            )
        except Exception as exc:
            issues.append(_pipeline_issue("write_narration_plan_failed", str(exc)))
            steps.append(
                PipelineStep(
                    name="write_narration_plan",
                    status="failed",
                    message=str(exc),
                )
            )
    else:
        steps.append(
            PipelineStep(
                name="write_narration_plan",
                status="skipped",
                message="Skipped because no narration plan was built.",
            )
        )

    report = _build_report(
        project_config=project_config,
        project_file=project_file,
        image_dir=image_dir,
        output_dir=output_dir,
        image_count=len(image_files),
        image_understanding_path=image_understanding_path,
        image_understanding_provider=image_provider_name,
        storyboard_path=storyboard_path,
        narration_plan_path=narration_plan_path,
        validation_passed=validation_passed,
        planner=planner_name,
        external_api_allowed=allow_external_api,
        external_api_called=external_api_called,
        image_understanding=image_understanding,
        storyboard=storyboard,
        storyboard_contract_report=storyboard_contract_report,
        storyboard_quality_report=storyboard_quality_report,
        narration_plan=narration_plan,
        tts_contract_report=tts_contract_report,
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
            image_understanding_path=image_understanding_path,
            image_understanding_provider=image_provider_name,
            storyboard_path=storyboard_path,
            narration_plan_path=narration_plan_path,
            validation_passed=validation_passed,
            planner=planner_name,
            external_api_allowed=allow_external_api,
            external_api_called=external_api_called,
            image_understanding=image_understanding,
            storyboard=storyboard,
            storyboard_contract_report=storyboard_contract_report,
            storyboard_quality_report=storyboard_quality_report,
            narration_plan=narration_plan,
            tts_contract_report=tts_contract_report,
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
            image_understanding_path=image_understanding_path,
            image_understanding_provider=image_provider_name,
            storyboard_path=storyboard_path,
            narration_plan_path=narration_plan_path,
            validation_passed=validation_passed,
            planner=planner_name,
            external_api_allowed=allow_external_api,
            external_api_called=external_api_called,
            image_understanding=image_understanding,
            storyboard=storyboard,
            storyboard_contract_report=storyboard_contract_report,
            storyboard_quality_report=storyboard_quality_report,
            narration_plan=narration_plan,
            tts_contract_report=tts_contract_report,
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


def write_image_understanding(
    output_dir: str | Path,
    image_understanding: ImageUnderstandingReport,
) -> Path:
    output_path = (
        Path(output_dir).expanduser().resolve() / IMAGE_UNDERSTANDING_FILE_NAME
    )
    _write_json(output_path, asdict(image_understanding))
    return output_path


def write_pipeline_report(output_dir: str | Path, report: PipelineReport) -> Path:
    report_path = Path(output_dir).expanduser().resolve() / PIPELINE_REPORT_FILE_NAME
    _write_json(report_path, pipeline_report_to_dict(report))
    return report_path


def write_narration_plan(output_dir: str | Path, narration_plan: NarrationPlan) -> Path:
    narration_plan_path = (
        Path(output_dir).expanduser().resolve() / NARRATION_PLAN_FILE_NAME
    )
    _write_json(narration_plan_path, asdict(narration_plan))
    return narration_plan_path


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
    image_understanding_path: str | None,
    image_understanding_provider: str,
    storyboard_path: str | None,
    narration_plan_path: str | None,
    validation_passed: bool,
    planner: str,
    external_api_allowed: bool,
    external_api_called: bool,
    image_understanding,
    storyboard,
    storyboard_contract_report,
    storyboard_quality_report,
    narration_plan,
    tts_contract_report,
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
        image_understanding_path=image_understanding_path,
        image_understanding_provider=image_understanding_provider,
        storyboard_path=storyboard_path,
        narration_plan_path=narration_plan_path,
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
        storyboard_contract_passed=(
            storyboard_contract_report.passed
            if storyboard_contract_report is not None
            else False
        ),
        storyboard_contract_errors=(
            [asdict(issue) for issue in storyboard_contract_report.errors]
            if storyboard_contract_report is not None
            else []
        ),
        storyboard_contract_warnings=(
            [asdict(issue) for issue in storyboard_contract_report.warnings]
            if storyboard_contract_report is not None
            else []
        ),
        duration_sum=(
            storyboard_contract_report.duration_sum
            if storyboard_contract_report is not None
            else 0
        ),
        storyboard_quality_passed=(
            storyboard_quality_report.passed
            if storyboard_quality_report is not None
            else False
        ),
        storyboard_quality_errors=(
            [asdict(issue) for issue in storyboard_quality_report.errors]
            if storyboard_quality_report is not None
            else []
        ),
        storyboard_quality_warnings=(
            [asdict(issue) for issue in storyboard_quality_report.warnings]
            if storyboard_quality_report is not None
            else []
        ),
        tts_contract_passed=(
            tts_contract_report.passed
            if tts_contract_report is not None
            else False
        ),
        tts_contract_errors=(
            [asdict(issue) for issue in tts_contract_report.errors]
            if tts_contract_report is not None
            else []
        ),
        tts_contract_warnings=(
            [asdict(issue) for issue in tts_contract_report.warnings]
            if tts_contract_report is not None
            else []
        ),
        narration_line_count=(
            len(narration_plan.lines) if narration_plan is not None else 0
        ),
        total_estimated_speech_seconds=(
            narration_plan.total_estimated_speech_seconds
            if narration_plan is not None
            else 0.0
        ),
        image_understanding_passed=(
            image_understanding is not None and not image_understanding.errors
        ),
        allowed_image_count=(
            image_understanding.allowed_image_count
            if image_understanding is not None
            else 0
        ),
        rejected_image_count=(
            image_understanding.rejected_image_count
            if image_understanding is not None
            else 0
        ),
        image_category_counts=(
            dict(image_understanding.category_counts)
            if image_understanding is not None
            else {}
        ),
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


def _contract_issues_to_pipeline_issues(contract_issues) -> list[dict[str, Any]]:
    return [
        {
            "code": issue.code,
            "message": issue.message,
            "severity": issue.level,
            "field": None,
            "file_name": None,
        }
        for issue in contract_issues
    ]


def _image_understanding_warnings_to_pipeline_issues(
    warnings: list[str],
) -> list[dict[str, Any]]:
    return [
        {
            "code": "image_understanding_warning",
            "message": warning,
            "severity": "warning",
            "field": "image_understanding",
            "file_name": None,
        }
        for warning in warnings
    ]


def _image_understanding_errors_to_pipeline_issues(
    errors: list[str],
) -> list[dict[str, Any]]:
    return [
        {
            "code": "image_understanding_error",
            "message": error,
            "severity": "error",
            "field": "image_understanding",
            "file_name": None,
        }
        for error in errors
    ]


def _has_failed_step(steps: list[PipelineStep], names: set[str]) -> bool:
    return any(step.name in names and step.status == "failed" for step in steps)


def _natural_sort_key(name: str) -> list[int | str]:
    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r"(\d+)", name)
    ]
