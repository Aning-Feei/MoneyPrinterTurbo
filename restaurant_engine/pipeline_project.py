from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import PIPELINE_REPORT_FILE_NAME, run_pipeline


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the restaurant_engine mock pipeline skeleton."
    )
    parser.add_argument(
        "project_arg",
        nargs="?",
        help="Path to project.json. Optional when --project is provided.",
    )
    parser.add_argument(
        "--project",
        dest="project_option",
        help="Path to project.json.",
    )
    parser.add_argument(
        "--planner",
        choices=("mock", "deepseek"),
        default="mock",
        help="Storyboard planner to use. Defaults to mock and does not call external APIs.",
    )
    parser.add_argument(
        "--image-understanding-provider",
        choices=("mock", "filename_fallback", "vision"),
        default="mock",
        help=(
            "Image understanding provider. Defaults to mock. The vision provider "
            "requires --allow-external-api and is not implemented yet."
        ),
    )
    parser.add_argument(
        "--allow-external-api",
        action="store_true",
        help="Allow explicit external API calls for planners such as deepseek.",
    )
    args = parser.parse_args()

    project_value = args.project_option or args.project_arg
    if not project_value:
        parser.error("project.json path is required as a positional argument or --project.")

    try:
        report = run_pipeline(
            Path(project_value).expanduser().resolve(),
            planner=args.planner,
            image_understanding_provider=args.image_understanding_provider,
            allow_external_api=args.allow_external_api,
        )
    except Exception as exc:
        print(f"pipeline failed: {exc}")
        return 2

    report_path = Path(report.output_dir) / PIPELINE_REPORT_FILE_NAME
    _print_summary(report, report_path)
    return 0 if report.ok else 1


def _print_summary(report, report_path: Path) -> None:
    print(f"project_id: {report.project_id}")
    print(f"ok: {report.ok}")
    print(f"planner: {report.planner}")
    print(f"external_api_allowed: {report.external_api_allowed}")
    print(f"external_api_called: {report.external_api_called}")
    print(f"validation_passed: {report.validation_passed}")
    print(f"target_duration_seconds: {report.target_duration_seconds}")
    print(f"image_count: {report.image_count}")
    print(f"image_understanding_provider: {report.image_understanding_provider}")
    print(
        "image_understanding_analysis_source: "
        f"{report.image_understanding_analysis_source}"
    )
    image_understanding_status = (
        "passed" if report.image_understanding_passed else "failed"
    )
    print(f"image_understanding: {image_understanding_status}")
    print(f"allowed_images: {report.allowed_image_count}")
    print(f"rejected_images: {report.rejected_image_count}")
    print(f"image_category_counts: {report.image_category_counts}")
    print(f"rule_engine_version: {report.rule_engine_version}")
    print(f"rule_engine_external_api_called: {report.rule_engine_external_api_called}")
    print(f"rule_engine_findings_count: {report.rule_engine_findings_count}")
    print(f"rule_engine_blocking: {report.rule_engine_blocking}")
    print(f"scene_count: {report.scene_count}")
    print(f"scene_durations: {report.scene_durations}")
    print(f"total_duration_seconds: {report.total_duration_seconds}")
    contract_status = "passed" if report.storyboard_contract_passed else "failed"
    print(f"storyboard contract: {contract_status}")
    print(f"duration_sum: {report.duration_sum}")
    print(f"contract errors count: {len(report.storyboard_contract_errors)}")
    print(f"contract warnings count: {len(report.storyboard_contract_warnings)}")
    quality_status = "passed" if report.storyboard_quality_passed else "failed"
    print(f"storyboard quality: {quality_status}")
    print(f"quality errors count: {len(report.storyboard_quality_errors)}")
    print(f"quality warnings count: {len(report.storyboard_quality_warnings)}")
    tts_status = "passed" if report.tts_contract_passed else "failed"
    print(f"tts contract: {tts_status}")
    print(f"tts errors count: {len(report.tts_contract_errors)}")
    print(f"tts warnings count: {len(report.tts_contract_warnings)}")
    print(f"narration_line_count: {report.narration_line_count}")
    print(f"total_estimated_speech_seconds: {report.total_estimated_speech_seconds}")
    print(f"output_dir: {report.output_dir}")
    print(f"image_understanding: {report.image_understanding_path}")
    print(f"rule_engine_report: {report.rule_engine_report_path}")
    print(f"storyboard: {report.storyboard_path}")
    print(f"narration_plan: {report.narration_plan_path}")
    print(f"pipeline_report: {report_path}")
    print("issues:")
    if report.issues:
        for issue in report.issues:
            severity = issue.get("severity", "error")
            code = issue.get("code", "unknown")
            message = issue.get("message", "")
            print(f"  - [{severity}] {code}: {message}")
    else:
        print("  - none")


if __name__ == "__main__":
    raise SystemExit(main())
