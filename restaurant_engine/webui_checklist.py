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
    video_aspect = _recommended_aspect(report, render_params)
    aspect_label = _format_video_aspect(video_aspect)

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
        "## 2. WebUI 页面操作步骤",
        "",
        "1. 打开 WebUI：`http://127.0.0.1:8501`",
        (
            "2. 在“视频来源”中选择："
            f"`{_format_video_source(video_source)}`，字段值：`video_source={video_source}`"
        ),
        "3. 在“上传本地文件”中按下方顺序上传图片",
        (
            "4. 在“视频拼接模式”中选择："
            f"`{_format_concat_mode(concat_mode)}`，字段值：`video_concat_mode={concat_mode}`"
        ),
        (
            "5. 在“视频片段最大时长(秒)”中填写："
            f"`{clip_duration}`，字段值：`video_clip_duration={clip_duration}`"
        ),
        f"6. 在“视频比例”中选择：`{aspect_label}`，字段值：`video_aspect={video_aspect}`",
        "7. 在“字幕设置”中开启：`启用字幕`，字段值：`subtitle_enabled=true`",
        "8. 检查音频设置，选择当前可用中文 TTS，不要在 checklist 中写死具体 voice_name",
        "9. 点击：`生成视频`",
        "",
        "## 3. 图片上传顺序",
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
            "## 4. 真实字段映射",
            "",
            "| WebUI 显示名称 | 后端字段 | 推荐值 |",
            "|---|---|---|",
            f"| 视频来源 | video_source | {video_source} |",
            "| 上传本地文件 | video_materials | 按图片顺序上传 |",
            f"| 视频拼接模式 | video_concat_mode | {concat_mode} |",
            f"| 视频片段最大时长(秒) | video_clip_duration | {clip_duration} |",
            f"| 视频比例 | video_aspect | {video_aspect} |",
            "| 启用字幕 | subtitle_enabled | true |",
            "| 字幕位置 | subtitle_position | bottom 或保持默认 |",
            "| 朗读声音 | voice_name | 根据当前可用中文 TTS 选择，不写死 |",
            "| 背景音乐 | bgm_type | 根据项目需要选择，不写死 |",
            "| 生成视频 | tm.start(...) | 点击按钮 |",
            "",
            "## 5. WebUI 参数摘要",
            "",
            f"- 拼接模式: {_format_concat_mode(concat_mode)}",
            f"- 每张图片时长: {clip_duration} 秒",
            f"- 素材来源: {_format_video_source(video_source)}",
            f"- 视频比例: {aspect_label}",
            "- 字幕: 启用字幕",
            "- 视频数量: 建议 1",
            "- 不要使用 Random。",
            "",
            "## 6. 旁白与时长",
            "",
            f"- 估算旁白时长: {estimated_seconds} 秒",
            f"- 图片总时长: {total_duration} 秒",
            f"- 是否存在循环风险: {_format_bool(will_loop)}",
            "",
            "## 7. 风险提示",
            "",
        ]
    )

    if ok and will_loop is not True:
        lines.extend(
            [
                "- 可以进入 WebUI 生成。",
                "- 请仍确认：未选择随机拼接，图片按顺序上传，clip duration 使用推荐值。",
            ]
        )
    else:
        lines.extend(
            [
                "- 不建议开始生成。",
                "- 请先修复图片数量、角色缺失或时长覆盖问题。",
                "- 不要依赖 Random 或自动循环补齐素材。",
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
            "## 8. 不要写死的字段",
            "",
            "以下字段不要机械照抄，应根据当前配置选择：",
            "",
            "- TTS 服务",
            "- 朗读声音 voice_name",
            "- 字幕字体",
            "- 背景音乐",
            "- 转场模式",
            "",
            "## 9. 生成前确认清单",
            "",
            "- [ ] WebUI 已打开",
            "- [ ] 视频来源选择 Local file / 本地文件",
            "- [ ] 图片已按顺序上传",
            "- [ ] 视频拼接模式选择 顺序拼接",
            "- [ ] 没有选择 随机拼接（推荐）",
            f"- [ ] 每张图片时长已设置为 {clip_duration} 秒",
            f"- [ ] 视频比例已确认：{aspect_label}",
            "- [ ] 字幕已启用",
            "- [ ] 音频/TTS 已确认",
            "- [ ] 旁白已确认",
            "- [ ] 点击生成视频前再次确认无循环风险",
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


def _recommended_aspect(report: dict[str, Any], render_params: dict[str, Any]) -> str:
    for value in (
        report.get("video_aspect"),
        report.get("aspect_ratio"),
        render_params.get("video_aspect"),
        render_params.get("aspect_ratio"),
    ):
        if value:
            return str(value)
    return "9:16"


def _format_video_aspect(value: Any) -> str:
    if str(value) == "9:16":
        return "竖屏 9:16（抖音视频）"
    if str(value) == "16:9":
        return "横屏 16:9（西瓜视频）"
    return f"{value} 或项目指定比例"


if __name__ == "__main__":
    raise SystemExit(main())
