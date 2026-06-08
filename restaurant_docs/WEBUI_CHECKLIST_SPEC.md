# WebUI 操作清单说明

## 目的

第 2 阶段 WebUI 操作清单工具用于把 `preflight_report.json` 转成人工可读的 WebUI 填表指南。

该工具只做 Markdown 文档生成，不调用外部 API，不生成视频，不读取 `storage/` 产物，也不修改 MoneyPrinterTurbo 原有业务代码。

## 输入

```bash
python3 -m restaurant_engine.webui_checklist /path/to/preflight_report.json
```

输入文件必须是预检器生成的 `preflight_report.json`。

## 输出

在 `preflight_report.json` 同目录生成：

```text
webui_checklist.md
```

`webui_checklist.md` 面向人工操作，包含：

- 项目信息
- 是否可以开始生成
- WebUI 页面操作步骤
- 图片上传顺序
- 真实 WebUI 字段映射
- WebUI 参数建议和选项值
- 旁白/时长检查
- 风险提示
- 不要写死的字段提示
- 生成前确认清单

后续 checklist 还应展示目标时长和动态时长约束：

- 目标视频时长
- 当前图片数量
- 合理图片数量范围
- 推荐 `video_clip_duration`
- 图片总覆盖时长
- 旁白最大中文字符数
- 文案一致性提醒
- WebUI 中实际 `video_script` 不得明显超过上限

## ok=true 行为

如果 `preflight_report.json` 中 `ok=true`：

- 明确写出可以进入 WebUI 生成
- 推荐使用 `Sequential / 顺序`
- 使用报告中的 `video_clip_duration`
- 明确提示不要使用 Random
- 明确提示打开 WebUI、选择 `Local file / 本地文件`、按顺序上传图片、点击 `生成视频`

## ok=false 行为

如果 `preflight_report.json` 中 `ok=false`：

- 仍然生成 `webui_checklist.md`
- 明确写出不建议开始生成
- 提示需要先修复图片数量、角色缺失或循环风险
- 保留 warnings/errors，方便人工逐项检查
- 明确提示不要依赖 Random 或自动循环补齐素材

## WebUI 字段映射

当前 checklist 会写出以下真实 WebUI 字段：

| WebUI 显示名称 | 后端字段 | 推荐值 |
|---|---|---|
| 视频来源 | video_source | local |
| 上传本地文件 | video_materials | 按图片顺序上传 |
| 视频拼接模式 | video_concat_mode | sequential |
| 视频片段最大时长(秒) | video_clip_duration | 预检推荐秒数 |
| 视频比例 | video_aspect | 9:16 或项目指定 |
| 启用字幕 | subtitle_enabled | true |
| 字幕位置 | subtitle_position | bottom 或保持默认 |
| 生成视频 | tm.start(...) | 点击按钮 |

以下字段不要写死，应根据当前 WebUI 配置选择：

- TTS 服务
- 朗读声音 voice_name
- 字幕字体
- 背景音乐
- 转场模式

## 目标时长和文案一致性提示

当 `preflight_report.json` 包含 `target_duration_seconds` 后，checklist 应明确写出：

- 用户选择的目标视频时长只能是 `30`、`40`、`50`、`60`。
- `video_clip_duration` 应按以下规则由 preflight 推荐：

```text
raw_clip_duration = ceil(target_duration_seconds / image_count)
recommended_clip_duration = clamp(raw_clip_duration, 3, 6)
total_image_duration = image_count * recommended_clip_duration
will_loop = total_image_duration < max(target_duration_seconds, estimated_narration_seconds)
```

- 推荐每张图 3-6 秒；低于 3 秒切换过快，高于 6 秒单图停留过久。
- 不建议依赖 random 或自动循环补齐素材。
- 如果 WebUI 中改写文案或 AI 生成了更长文案，必须重新跑 preflight。

旁白字数安全上限：

```text
narration_safe_seconds = target_duration_seconds - 3
narration_max_cjk_chars = floor(narration_safe_seconds * 4.0)
```

参考表：

| 目标时长 | 旁白安全秒数 | 最大中文字符数 |
|---|---:|---:|
| 30 秒 | 27 秒 | 约 108 字 |
| 40 秒 | 37 秒 | 约 148 字 |
| 50 秒 | 47 秒 | 约 188 字 |
| 60 秒 | 57 秒 | 约 228 字 |

checklist 应提醒人工确认 WebUI 实际 `video_script` 不明显超过该上限。

## 当前限制

- 不会自动操作 WebUI。
- 不会读取图片内容。
- 不会生成视频。
- 不会保证人工填写时不出错。
- 只根据 `preflight_report.json` 生成清单。
