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
    print(f"scene_count: {report.scene_count}")
    print(f"scene_durations: {report.scene_durations}")
    print(f"total_duration_seconds: {report.total_duration_seconds}")
    contract_status = "passed" if report.storyboard_contract_passed else "failed"
    print(f"storyboard contract: {contract_status}")
    print(f"duration_sum: {report.duration_sum}")
    print(f"contract errors count: {len(report.storyboard_contract_errors)}")
    print(f"contract warnings count: {len(report.storyboard_contract_warnings)}")
    print(f"output_dir: {report.output_dir}")
    print(f"storyboard: {report.storyboard_path}")
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
