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
- 图片上传顺序
- WebUI 参数建议
- 旁白/时长检查
- 风险提示
- 生成前确认清单

## ok=true 行为

如果 `preflight_report.json` 中 `ok=true`：

- 明确写出可以进入 WebUI 生成
- 推荐使用 `Sequential / 顺序`
- 使用报告中的 `video_clip_duration`
- 明确提示不要使用 Random

## ok=false 行为

如果 `preflight_report.json` 中 `ok=false`：

- 仍然生成 `webui_checklist.md`
- 明确写出不建议开始生成
- 提示需要先修复图片数量、角色缺失或循环风险
- 保留 warnings/errors，方便人工逐项检查

## 当前限制

- 不会自动操作 WebUI。
- 不会读取图片内容。
- 不会生成视频。
- 不会保证人工填写时不出错。
- 只根据 `preflight_report.json` 生成清单。
