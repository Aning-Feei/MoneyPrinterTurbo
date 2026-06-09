# 第 4 阶段本地封面渲染 Contract

本文件记录 TwinkleBite AI 餐饮宣传视频第 4 阶段封面生成模块的本地渲染骨架。

当前任务是在 `cover_plan.json` 已确定标题和封面候选图之后，使用本地 Pillow / PIL 生成一张基础封面图。

## 当前范围

- 输入来自 `cover_plan.json`。
- 使用 `selected_title.text` / `cover_copy.title` 作为封面主标题。
- 使用 `selected_assets.primary_image_path` 指向的用户上传图片作为底图。
- 输出 `cover_image.png`。
- 输出 `cover_render_report.json`。
- 将封面渲染摘要写入 `pipeline_report.json`。

当前不做：

- 不接 AI 图片生成。
- 不调用 DeepSeek。
- 不调用任何外部 API。
- 不读取 API Key。
- 不调用视觉模型。
- 不做图片内容理解。
- 不调用 TTS。
- 不生成音频。
- 不生成视频。
- 不修改 WebUI。
- 不安装依赖。

## Renderer

当前 renderer：

```text
local_pillow
```

要求：

- 只使用当前环境中已存在的 Pillow / PIL。
- 不安装 Pillow。
- 不修改 `requirements.txt` / `pyproject.toml` / lock 文件。
- 不下载字体。
- 不复制或提交字体文件。

如果运行 pipeline 的 Python 环境无法 import PIL，renderer 会受控失败并在 `cover_render_report.json` 中记录 `PIL_UNAVAILABLE`。

## 输出文件

成功路径输出：

```text
output/cover_image.png
output/cover_render_report.json
```

图片规格：

- 格式：PNG
- 尺寸：1080 x 1920
- 比例：9:16

渲染策略：

- 打开 `selected_assets.primary_image_path`。
- center crop / resize 到 1080 x 1920。
- 添加轻量暗色遮罩和标题背景区域。
- 在上方区域绘制 `selected_title.text`。
- 标题过长时做简单换行。

## 输入校验

渲染前必须校验：

- `cover_plan.selected_title.text` 存在。
- `cover_plan.cover_copy.title` 存在。
- `cover_plan.cover_copy.title == cover_plan.selected_title.text`。
- `cover_plan.selected_assets.primary_image_id` 存在。
- `cover_plan.selected_assets.primary_image_path` 存在。
- `primary_image_path` 指向的文件存在。
- `primary_image_path` 来自 `image_understanding` contract 中的已知用户上传图片。

失败行为：

- title 不一致：`render_status=failed`，warning `TITLE_MISMATCH`，`blocking=true`。
- 图片不存在：`render_status=failed`，warning `SOURCE_IMAGE_NOT_FOUND`，`blocking=true`。
- 图片不在 contract 中：`render_status=failed`，warning `SOURCE_IMAGE_NOT_IN_CONTRACT`，`blocking=true`。
- PIL 不可用：`render_status=failed`，warning `PIL_UNAVAILABLE`，`blocking=true`。

## cover_render_report.json

顶层字段：

- `version`
- `renderer`
- `external_api_called`
- `render_status`
- `cover_image_path`
- `output_format`
- `output_width`
- `output_height`
- `source_cover_plan_path`
- `source_image_id`
- `source_image_path`
- `title_text`
- `title_source`
- `used_font`
- `warnings`
- `blocking`

成功路径固定：

- `renderer=local_pillow`
- `external_api_called=false`
- `render_status=rendered`
- `output_format=png`
- `output_width=1080`
- `output_height=1920`
- `title_source=selected_title`
- `blocking=false`

## 字体

renderer 会优先尝试系统中文字体，例如：

- `PingFang.ttc`
- `STHeiti Light.ttc`
- `STHeiti Medium.ttc`
- `Arial Unicode.ttf`

如果没有可用字体，使用 PIL 默认字体，并记录：

```text
FONT_FALLBACK_USED
```

字体文件不复制进仓库，不提交进 Git。

## pipeline_report 字段

`pipeline_report.json` 新增封面渲染字段：

- `cover_render_report_path`
- `cover_renderer`
- `cover_render_external_api_called`
- `cover_render_status`
- `cover_rendered_image_path`
- `cover_render_output_width`
- `cover_render_output_height`
- `cover_render_source_image_id`
- `cover_render_title_text`
- `cover_render_blocking`

## 与 cover_plan 的关系

当前采用保守方案：

- `cover_plan.json` 保持原始封面方案 contract。
- `cover_plan.render_status` 仍可保持 `not_rendered`。
- 真实渲染结果写入 `cover_render_report.json` 和 `pipeline_report.json`。

## 安全边界

- 默认不调用任何外部 API。
- 不调用 DeepSeek。
- 不调用任何 LLM。
- 不调用 AI 图片生成。
- 不读取 API Key。
- 不下载字体。
- 不安装依赖。
- 不生成音频。
- 不生成视频。
- 不修改 WebUI / `app/` / `config.toml` / `storage/` / `resource/`。

## 当前测试边界

- Smoke test 输出只允许放在仓库外 `/private/tmp` 或外部样本 `output/`。
- 不提交 `cover_image.png`。
- 不提交 `cover_render_report.json` 或任何 output 产物。
- 本轮暂不 commit，等待后续提交前复核。
