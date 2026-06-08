from __future__ import annotations

import argparse
from pathlib import Path

from .validator import report_to_dict, validate_project, write_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate restaurant video project input.")
    parser.add_argument("--project", required=True, help="Path to project.json")
    args = parser.parse_args()

    project_path = Path(args.project).expanduser().resolve()
    report = validate_project(project_path)
    output_path = project_path.parent / "validation_report.json"
    write_report(report, output_path)
    _print_report(report_to_dict(report), str(output_path))
    return 0 if report.passed else 1


def _print_report(report: dict, output_path: str) -> None:
    print(f"project_path: {report['project_path']}")
    print(f"project_name: {report['project_name']}")
    print(f"image_dir: {report['image_dir']}")
    print(f"image_count: {report['image_count']}")
    print("image_files:")
    for file_name in report["image_files"]:
        print(f"  - {file_name}")

    print("category_checks:")
    for category, passed in report["category_checks"].items():
        print(f"  - {category}: {passed}")

    print("issues:")
    if report["issues"]:
        for issue in report["issues"]:
            print(f"  - [{issue['severity']}] {issue['code']}: {issue['message']}")
    else:
        print("  - none")

    print(f"passed: {report['passed']}")
    print(f"validation_report: {output_path}")


if __name__ == "__main__":
    raise SystemExit(main())
