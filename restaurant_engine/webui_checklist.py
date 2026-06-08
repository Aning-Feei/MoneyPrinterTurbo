from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_preflight_report(report_path: str | Path) -> dict[str, Any]:
    report_file = Path(report_path).expanduser().resolve()
    data = json.loads(report_file.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("preflight_report.json must contain a JSON object")
    return data


def build_webui_checklist(report: dict[str, Any]) -> str:
    project_id = str(report.get("project_id") or "unknown")
    ok = bool(report.get("ok"))
    shot_plan = _as_dict(report.get("shot_plan"))
    timing = _as_dict(report.get("timing"))
    render_params = _as_dict(report.get("render_params"))
    issues = report.get("issues") if isinstance(report.get("issues"), list) else []
    shots = shot_plan.get("shots") if isinstance(shot_plan.get("shots"), list) else []

    estimated_seconds = timing.get("estimated_narration_seconds", "unknown")
    clip_duration = render_params.get(
        "video_clip_duration", timing.get("recommended_clip_duration", "unknown")
    )
    video_source = render_params.get("video_source", "local")
    concat_mode = render_params.get("video_concat_mode", "sequential")
    will_loop = timing.get("will_loop", "unknown")
    total_duration = shot_plan.get("total_image_duration", "unknown")

    start_recommendation = "可以进入 WebUI 生成" if ok else "不建议开始生成"
    status_note = (
        "预检通过。请按下方顺序和参数进入 WebUI。"
        if ok
        else "预检未通过。请先修复图片数量、角色缺失或循环风险。"
    )

    lines = [
        "# WebUI 操作清单",
        "",
        "## 1. 项目状态",
        "",
        f"- Project ID: {project_id}",
        f"- 是否通过预检: {_format_bool(ok)}",
        f"- 是否建议开始生成: {start_recommendation}",
        f"- 状态说明: {status_note}",
        "",
        "## 2. 图片上传顺序",
        "",
    ]

    if shots:
        for index, shot in enumerate(shots, start=1):
            shot_data = _as_dict(shot)
            image_name = shot_data.get("image_name", "unknown")
            role = shot_data.get("role", "unknown")
            duration = shot_data.get("recommended_duration", clip_duration)
            lines.append(f"{index}. {image_name} ({role}, {duration}s)")
    else:
        lines.append("- 未发现可上传图片。")

    lines.extend(
        [
            "",
            "## 3. WebUI 参数",
            "",
            f"- 拼接模式: {_format_concat_mode(concat_mode)}",
            f"- 每张图片时长: {clip_duration} 秒",
            f"- 素材来源: {_format_video_source(video_source)}",
            "- 不要使用 Random。",
            "",
            "## 4. 旁白与时长",
            "",
            f"- 估算旁白时长: {estimated_seconds} 秒",
            f"- 图片总时长: {total_duration} 秒",
            f"- 是否存在循环风险: {_format_bool(will_loop)}",
            "",
            "## 5. 风险提示",
            "",
        ]
    )

    if issues:
        for issue in issues:
            issue_data = _as_dict(issue)
            severity = issue_data.get("severity", "unknown")
            code = issue_data.get("code", "unknown")
            message = issue_data.get("message", "")
            lines.append(f"- [{severity}] {code}: {message}")
    else:
        lines.append("- 未发现 warnings/errors。")

    lines.extend(
        [
            "",
            "## 6. 生成前确认",
            "",
            "- [ ] 图片已按顺序上传",
            "- [ ] 拼接模式已选择 Sequential / 顺序",
            f"- [ ] 每张图片时长已设置为 {clip_duration} 秒",
            "- [ ] 未选择 Random",
            "- [ ] 旁白已确认",
        ]
    )

    if not ok:
        lines.extend(
            [
                "- [ ] 已修复图片数量、角色缺失或循环风险",
                "- [ ] 修复后已重新运行 preflight_project",
            ]
        )

    return "\n".join(lines) + "\n"


def write_webui_checklist(markdown: str, output_path: str | Path) -> None:
    output_file = Path(output_path).expanduser().resolve()
    output_file.write_text(markdown, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a manual WebUI checklist from preflight_report.json."
    )
    parser.add_argument("report", help="Path to preflight_report.json")
    args = parser.parse_args()

    try:
        report_path = Path(args.report).expanduser().resolve()
        report = load_preflight_report(report_path)
        markdown = build_webui_checklist(report)
        output_path = report_path.parent / "webui_checklist.md"
        write_webui_checklist(markdown, output_path)
    except Exception as exc:
        print(f"webui checklist failed: {exc}")
        return 2

    print(f"webui_checklist: {output_path}")
    if report.get("ok"):
        print("checklist generated: 可以进入 WebUI 生成")
    else:
        print("checklist generated with validation warnings: 不建议开始生成")
    return 0


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _format_bool(value: Any) -> str:
    if value is True:
        return "是"
    if value is False:
        return "否"
    return str(value)


def _format_concat_mode(value: Any) -> str:
    if str(value).lower() == "sequential":
        return "Sequential / 顺序"
    if str(value).lower() == "random":
        return "Random / 随机（不建议）"
    return str(value)


def _format_video_source(value: Any) -> str:
    if str(value).lower() == "local":
        return "Local file / 本地文件"
    return str(value)


if __name__ == "__main__":
    raise SystemExit(main())
