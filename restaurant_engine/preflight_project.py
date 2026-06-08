from __future__ import annotations

import argparse
from pathlib import Path

from .preflight import (
    preflight_report_to_dict,
    run_preflight,
    write_preflight_report,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build restaurant video preflight recommendations."
    )
    parser.add_argument("project", help="Path to project.json")
    args = parser.parse_args()

    try:
        project_path = Path(args.project).expanduser().resolve()
        report = run_preflight(project_path)
        output_path = project_path.parent / "preflight_report.json"
        write_preflight_report(report, output_path)
        report_data = preflight_report_to_dict(report)
        _print_summary(report_data, output_path)
    except Exception as exc:
        print(f"preflight failed: {exc}")
        return 2

    if report.ok:
        print("preflight completed successfully")
        return 0

    print("preflight completed with validation errors: 预检已完成，但存在校验错误")
    return 1


def _print_summary(report: dict, output_path: Path) -> None:
    print(f"project_id: {report['project_id']}")
    print(f"ok: {report['ok']}")
    print(f"estimated_narration_seconds: {report['timing']['estimated_narration_seconds']}")
    print(f"recommended_clip_duration: {report['timing']['recommended_clip_duration']}")
    print(f"will_loop: {report['timing']['will_loop']}")
    print("recommended_webui_params:")
    print(f"  video_source: {report['render_params']['video_source']}")
    print(f"  video_concat_mode: {report['render_params']['video_concat_mode']}")
    print(f"  video_clip_duration: {report['render_params']['video_clip_duration']}")
    print("shots:")
    for shot in report["shot_plan"]["shots"]:
        print(
            "  - "
            f"{shot['index']}. {shot['role']} | {shot['image_name']} | "
            f"{shot['recommended_duration']}s"
        )
    print("issues:")
    if report["issues"]:
        for issue in report["issues"]:
            print(f"  - [{issue['severity']}] {issue['code']}: {issue['message']}")
    else:
        print("  - none")
    print(f"preflight_report: {output_path}")


if __name__ == "__main__":
    raise SystemExit(main())
