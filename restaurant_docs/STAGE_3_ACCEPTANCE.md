# 第 3 阶段验收：图片理解与规则引擎 Contract 冻结

本文件记录餐饮 AI 宣传视频生成系统第 3 阶段“图片理解与规则引擎”的收口验收结果。第 3 阶段的产物将作为第 4 阶段封面生成模块的输入 contract。

## 阶段范围

第 3 阶段已完成：

- `image_understanding` provider 架构。
- `mock` / `filename_fallback` / `vision` provider 模式。
- 默认 `mock` provider。
- `filename_fallback` 显式 fallback provider。
- `vision` provider stub。
- 本地 `local_static` rule engine。
- `image_understanding.json` 输出 contract。
- `rule_engine_report.json` 输出 contract。
- `pipeline_report.json` 中图片理解与规则引擎状态字段。
- 本地 smoke 验收。

第 3 阶段不包含：

- 真实视觉模型。
- 真实图片内容理解。
- 封面生成。
- TTS。
- 音频生成。
- 视频生成。
- WebUI 改造。
- 外部 API 调用。

## 已完成提交

- `ef33a97 feat: add image understanding provider architecture`
- `a6487e2 feat: add local rule engine contract`

## Provider Contract

### mock

- 默认 provider。
- 不读取图片像素内容。
- 不使用文件名语义。
- 不调用外部 API。
- `provider=mock`。
- `analysis_source=mock`。
- `external_api_called=false`。
- 单图 `source=mock`。
- 单图 `detected_type=unknown`。
- `category_counts` 通常为 `unknown`。
- 用于本地开发占位和 contract 联调。

### filename_fallback

- 必须显式使用 `--image-understanding-provider filename_fallback`。
- 不读取图片像素内容。
- 使用文件名规则进行开发兜底分类。
- 不调用外部 API。
- `provider=filename_fallback`。
- `analysis_source=filename_fallback`。
- `external_api_called=false`。
- 单图 `source=filename_fallback`。
- 可根据文件名产生 `intro` / `interior` / `dish` / `dining` / `detail` / `extra` 等分类。
- 该 provider 不是正式图片内容理解逻辑。

### vision

- 未来真实图片内容理解入口。
- 未带 `--allow-external-api` 时 fail fast。
- 带 `--allow-external-api` 时当前仍 controlled fail / NotImplemented。
- 当前不读取 API Key。
- 当前不联网。
- 当前不调用 SDK。
- 当前不调用 DeepSeek。
- 当前不生成 `image_understanding.json` 成功结果。

## Rule Engine Contract

当前规则引擎：

- `engine=local_static`
- `external_api_called=false`
- 只消费 `image_understanding` 输出。
- 不重新读取文件名。
- 不重新根据文件名分类。
- 不读取图片像素内容。
- 不调用外部 API。
- 不读取 API Key。
- `blocking=false`。

`mock` provider 下：

- findings 包含 `NO_CONTENT_BASED_UNDERSTANDING`。
- `summary.has_content_based_understanding=false`。
- `summary.has_filename_fallback=false`。
- `storyboard_hints.requires_human_review=true`。

`filename_fallback` provider 下：

- findings 包含 `FILENAME_FALLBACK_USED`。
- `summary.has_content_based_understanding=false`。
- `summary.has_filename_fallback=true`。
- `storyboard_hints.requires_human_review=true`。

## Output Contract

第 3 阶段成功路径输出：

- `image_understanding.json`
- `rule_engine_report.json`
- `storyboard.json`
- `narration_plan.json`
- `pipeline_report.json`

### image_understanding.json

第 4 阶段可依赖：

- `provider`
- `analysis_source`
- `external_api_called`
- `images`
- 单图 `image_id`
- 单图 `image_path`
- 单图 `detected_type`
- 单图 `source`
- 单图 `quality_score`
- 单图 `cover_score`
- 单图 `video_score`
- 单图 `risk_score`
- 单图 `reason`
- 顶层 `category_counts`
- 顶层 `notes`

### rule_engine_report.json

第 4 阶段可依赖：

- `version`
- `engine`
- `external_api_called`
- `image_understanding_provider`
- `image_understanding_analysis_source`
- `summary.image_count`
- `summary.category_counts`
- `summary.has_content_based_understanding`
- `summary.has_filename_fallback`
- `findings`
- `asset_groups.hero_candidates`
- `asset_groups.dish_candidates`
- `asset_groups.interior_candidates`
- `asset_groups.fallback_candidates`
- `storyboard_hints.preferred_opening_image_id`
- `storyboard_hints.avoid_repeating_same_image`
- `storyboard_hints.requires_human_review`
- `blocking`

### pipeline_report.json

第 4 阶段可依赖：

- `image_understanding_provider`
- `image_understanding_analysis_source`
- `external_api_called`
- `rule_engine_report_path`
- `rule_engine_external_api_called`
- `rule_engine_findings_count`
- `rule_engine_blocking`
- `rule_engine_version`

## 第 4 阶段不得假设

第 4 阶段封面生成模块不得假设：

- 已经有真实图片内容理解。
- `detected_type` 一定准确。
- `filename_fallback` 是正式分类能力。
- `requires_human_review=false`。
- 可以调用外部 API。
- 可以读取 API Key。
- 可以生成音频。
- 可以生成视频。
- storyboard planner 已经消费 `rule_engine_report`。

## Smoke Test 摘要

第 3 阶段 contract freeze 验收覆盖：

- 默认 `mock` provider：通过。
- 显式 `mock` provider：通过。
- `filename_fallback` provider：通过。
- `vision` 未授权：受控失败。
- `vision --allow-external-api`：受控未实现失败。
- `python3 -m compileall restaurant_engine`：通过。
- `.venv/bin/python -m compileall restaurant_engine`：通过。
- 当前仓库无 `tests/` 目录，未执行 pytest。

所有 smoke test 均使用 mock planner，不使用 DeepSeek planner，不调用外部 API，不调用 TTS，不生成音频，不生成视频。

## 已知限制

- `mock` 不理解图片内容。
- `filename_fallback` 依赖文件名，只能作为 fallback。
- `vision` 未接真实模型。
- rule engine 当前只是本地静态规则。
- 当前 rule engine 不阻断 pipeline。
- 当前 storyboard 不强制消费 `rule_engine_report`。
- 当前未生成视频。

## 进入第 4 阶段条件

- 第 3 阶段 contract freeze 验收通过。
- 第 4 阶段只消费本文件列出的现有 contract 字段。
- 第 4 阶段默认仍不调用外部 API。
- 第 4 阶段不得把 `filename_fallback` 当作正式图片内容理解。

## 第 4 阶段启动说明

- 第 4 阶段封面生成模块已开始。
- 第一版只消费第 3 阶段冻结的 `image_understanding` 和 `rule_engine_report` contract。
- 当前新增 `cover_plan.json`，用于记录标题候选、用户选择标题和封面候选图。
- 当前不生成真实封面图片，不调用外部 API，不读取图片像素，不改变第 3 阶段验收结论。
