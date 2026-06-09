# Rule Engine Contract 说明

本文件记录第 3 阶段本地规则引擎骨架。规则引擎位于 `image_understanding.json` 之后、`storyboard.json` 之前，用于把图片理解结果转换为后续 storyboard 可消费的本地决策信号。

第 3 阶段 contract freeze 与第 4 阶段可依赖字段见：

- `restaurant_docs/STAGE_3_ACCEPTANCE.md`

## 当前目标

- 读取 pipeline 已生成的 `image_understanding` 结果。
- 不重新读取图片文件名。
- 不读取图片像素内容。
- 不调用 DeepSeek、视觉模型、TTS 或任何外部 API。
- 输出 `rule_engine_report.json`。
- 在 `pipeline_report.json` 中记录规则引擎摘要。

## 输入

规则引擎只消费 `ImageUnderstandingReport`：

- `provider`
- `images`
- `category_counts`
- 每张图片的 `image_id`
- 每张图片的 `detected_type`
- 每张图片的 `source`

当前规则引擎不依赖文件名判断图片类别。文件名 fallback 如果存在，也必须来自上游 `image_understanding` 的显式结果，并标记为 `source=filename_fallback`。

## 输出

`rule_engine_report.json` 顶层字段：

- `version`
- `engine`
- `external_api_called`
- `image_understanding_provider`
- `image_understanding_analysis_source`
- `summary`
- `findings`
- `asset_groups`
- `storyboard_hints`
- `blocking`

当前固定：

- `engine=local_static`
- `external_api_called=false`
- `blocking=false`

## Summary

`summary` 记录：

- `image_count`
- `category_counts`
- `has_content_based_understanding`
- `has_filename_fallback`

当前含义：

- `mock`：`has_content_based_understanding=false`，`has_filename_fallback=false`。
- `filename_fallback`：`has_content_based_understanding=false`，`has_filename_fallback=true`。
- `vision`：未来接入真实视觉模型后，才代表 `has_content_based_understanding=true`。

## Findings

当前 findings 只做提示，不阻断 pipeline：

- `NO_CONTENT_BASED_UNDERSTANDING`：mock provider，仅开发占位，没有图片内容理解。
- `FILENAME_FALLBACK_USED`：filename fallback provider，仅文件名兜底，不是正式图片理解。
- `UNKNOWN_IMAGE_UNDERSTANDING_PROVIDER`：未知 provider，要求人工复核。

## Asset Groups

`asset_groups` 用于给 storyboard planner 提供候选图片组：

- `hero_candidates`
- `dish_candidates`
- `interior_candidates`
- `fallback_candidates`

当前分组只基于上游 `detected_type`：

- hero：`intro` / `storefront` / `exterior` / `hero`
- dish：`dish` / `food` / `menu_item` / `menu`
- interior：`interior` / `dining` / `environment`
- 其他类型进入 fallback

## Storyboard Hints

`storyboard_hints` 记录：

- `preferred_opening_image_id`
- `avoid_repeating_same_image`
- `requires_human_review`

当前规则：

- 优先使用第一个 hero candidate 作为 opening image。
- 没有 hero candidate 时，使用第一个 fallback candidate。
- `avoid_repeating_same_image=true`。
- 非 `vision` provider 均要求 `requires_human_review=true`。

## Pipeline Report 字段

`pipeline_report.json` 记录：

- `rule_engine_report_path`
- `rule_engine_external_api_called`
- `rule_engine_findings_count`
- `rule_engine_blocking`
- `rule_engine_version`

## 安全边界

- 默认 pipeline 不调用外部 API。
- `mock` 与 `filename_fallback` provider 均可生成 `rule_engine_report.json`。
- `vision` 未授权时会在 image understanding 阶段被阻止，不生成 rule engine report。
- `vision` 授权但当前未实现时也不会调用外部 API，不生成 rule engine report。
- 本阶段不生成视频、不调用 TTS、不调用图生视频。
- 第 4 阶段不得假设已经有真实图片内容理解，也不得把 `filename_fallback` 当作正式分类能力。
