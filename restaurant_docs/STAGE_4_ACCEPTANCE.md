# 第 4 阶段验收：封面生成 Contract 冻结

本文件记录餐饮 AI 宣传视频生成系统第 4 阶段“封面生成模块”的收口验收结果。第 4 阶段产物将作为第 5 阶段“分镜脚本与口播文案生成”的输入 contract。

## 阶段范围

第 4 阶段已完成：

- `theme_text` 到 3 个本地标题候选。
- 支持用户通过 `selected_cover_title_id` / `selected_cover_title` 选择标题。
- 无选择时默认 `title_1`。
- 无效选择时 fallback 到 `title_1` 并记录 warning。
- `selected_title.text` 作为封面主标题。
- `cover_copy.title == selected_title.text`。
- 从用户上传图片 contract 中选择封面候选图。
- 输出 `cover_plan.json`。
- 使用本地 Pillow / PIL 输出 `cover_image.png`。
- 输出 `cover_render_report.json`。
- 将 cover plan / cover render 摘要写入 `pipeline_report.json`。
- 本地 smoke 验收。

第 4 阶段不包含：

- AI 图片生成。
- 真实视觉模型。
- 真实图片内容理解。
- DeepSeek 调用。
- 外部 API 调用。
- TTS。
- 音频生成。
- 视频生成。
- WebUI 改造。
- Web 正式产品形态。

## 已完成提交

- `d517160 feat: add local cover plan contract`
- `7bea98d feat: add local cover renderer`

## Cover Plan Contract

第 5 阶段可以依赖 `cover_plan.json` 顶层字段：

- `version`
- `planner`
- `external_api_called`
- `render_status`
- `cover_image_path`
- `source_contracts`
- `title_generation`
- `title_candidates`
- `selected_title`
- `selected_assets`
- `cover_copy`
- `layout`
- `quality_flags`
- `warnings`
- `blocking`

关键子结构：

- `title_generation.theme_text`
- `title_generation.title_provider`
- `title_generation.external_api_called`
- `title_candidates[].title_id`
- `title_candidates[].text`
- `title_candidates[].source`
- `title_candidates[].selected`
- `selected_title.title_id`
- `selected_title.text`
- `selected_title.user_selected`
- `selected_title.selection_source`
- `selected_assets.primary_image_id`
- `selected_assets.primary_image_path`
- `selected_assets.primary_asset_group`
- `selected_assets.selection_reason`
- `selected_assets.user_selected_image`
- `selected_assets.fallback_used`
- `cover_copy.title`
- `cover_copy.subtitle`
- `cover_copy.cta`
- `cover_copy.language`
- `cover_copy.copy_source`
- `layout.format`
- `layout.safe_area`
- `layout.text_zones`
- `quality_flags.requires_human_review`
- `quality_flags.content_based_understanding`
- `quality_flags.uses_filename_fallback`
- `quality_flags.has_primary_image`
- `quality_flags.has_user_selected_title`

当前固定语义：

- `planner=local_static`
- `external_api_called=false`
- `title_generation.title_provider=local_static`
- `cover_copy.title == selected_title.text`
- `selected_assets.primary_image_path` 来自用户上传图片 contract。
- `quality_flags.requires_human_review=true`
- `cover_plan.render_status` 仍描述原始封面方案状态，不作为最终渲染结果来源。

## Cover Render Contract

第 5 阶段可以依赖 `cover_render_report.json` 顶层字段：

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

成功路径固定语义：

- `renderer=local_pillow`
- `external_api_called=false`
- `render_status=rendered`
- `cover_image_path` 指向 `cover_image.png`
- `output_format=png`
- `output_width=1080`
- `output_height=1920`
- `source_image_id == cover_plan.selected_assets.primary_image_id`
- `source_image_path == cover_plan.selected_assets.primary_image_path`
- `title_text == cover_plan.selected_title.text`
- `title_source=selected_title`
- `blocking=false`

异常路径已文档化：

- `TITLE_MISMATCH`
- `SOURCE_IMAGE_NOT_FOUND`
- `SOURCE_IMAGE_NOT_IN_CONTRACT`
- `PIL_UNAVAILABLE`
- `FONT_FALLBACK_USED`

## Output Contract

第 4 阶段成功路径输出：

- `image_understanding.json`
- `rule_engine_report.json`
- `cover_plan.json`
- `cover_render_report.json`
- `cover_image.png`
- `storyboard.json`
- `narration_plan.json`
- `pipeline_report.json`

`cover_image.png` 当前为本地 Pillow 渲染图片：

- PNG
- 1080 x 1920
- 9:16

## pipeline_report Cover 字段

第 5 阶段可以依赖 `pipeline_report.json` 中的 cover plan 字段：

- `cover_plan_path`
- `cover_planner`
- `cover_external_api_called`
- `cover_render_status`
- `cover_image_path`
- `cover_selected_image_id`
- `cover_selected_title`
- `cover_title_candidates_count`
- `cover_title_user_selected`
- `cover_requires_human_review`
- `cover_blocking`

第 5 阶段可以依赖 `pipeline_report.json` 中的 cover render 字段：

- `cover_render_report_path`
- `cover_renderer`
- `cover_render_external_api_called`
- `cover_rendered_image_path`
- `cover_render_output_width`
- `cover_render_output_height`
- `cover_render_source_image_id`
- `cover_render_title_text`
- `cover_render_blocking`

## 第 5 阶段可依赖字段

第 5 阶段可以消费：

- `cover_plan.selected_title.text`
- `cover_plan.cover_copy.title`
- `cover_plan.title_candidates`
- `cover_plan.selected_assets.primary_image_id`
- `cover_plan.selected_assets.primary_image_path`
- `cover_render_report.cover_image_path`
- `cover_render_report.title_text`
- `cover_render_report.source_image_id`
- `cover_render_report.output_width`
- `cover_render_report.output_height`
- `pipeline_report.cover_rendered_image_path`
- `pipeline_report.cover_render_title_text`

第 5 阶段应优先使用 `cover_render_report` / `pipeline_report` 中的渲染结果判断真实封面图状态，不应假设 `cover_plan.cover_image_path` 已回写。

## 第 5 阶段不得假设

第 5 阶段不得假设：

- 已经有真实图片内容理解。
- `detected_type` 一定准确。
- `filename_fallback` 是正式分类能力。
- `cover_image.png` 是 AI 生成图片。
- 可以调用外部 API。
- 可以调用 DeepSeek。
- 可以调用 TTS。
- 可以生成音频。
- 可以生成视频。
- 可以改 WebUI。
- WebUI 是最终产品。
- `requires_human_review=false`。

## Smoke Test 摘要

第 4 阶段 contract freeze 验收覆盖：

- 默认 `mock` provider + `selected_cover_title_id`：通过。
- 默认 `mock` provider + 无用户选择标题：通过。
- 默认 `mock` provider + 无效标题选择：通过。
- `filename_fallback` provider：通过。
- `vision` 未授权：受控失败。
- `vision --allow-external-api` 当前未实现：受控失败。
- `cover_image.png` 存在性 / PNG / 1080 x 1920：通过。
- `python3 -m compileall restaurant_engine`：通过。
- `.venv/bin/python -m compileall restaurant_engine`：通过。
- 当前仓库无 `tests/` 目录，未执行 pytest。

所有 smoke test 均使用 mock planner，不使用 DeepSeek planner，不调用外部 API，不调用 TTS，不生成音频，不生成视频。封面图片只生成在仓库外 `/private/tmp` smoke output 中。

## 已知限制

- 当前封面是本地 Pillow 渲染，不是 AI 生成。
- 当前封面设计很基础，只用于 contract 联调。
- 当前依赖第 3 阶段非真实视觉 contract。
- 当前 `requires_human_review=true`。
- 当前未生成音频。
- 当前未生成视频。
- 当前未接 TTS。
- 当前未接真实视觉模型。

## 进入第 5 阶段条件

- 第 4 阶段 contract freeze 验收通过。
- 第 5 阶段只消费本文件列出的现有 contract 字段。
- 第 5 阶段默认仍不调用外部 API。
- 第 5 阶段不得把 `filename_fallback` 当作正式图片内容理解。
- 第 5 阶段不得把 `cover_image.png` 当作 AI 图片生成结果。
