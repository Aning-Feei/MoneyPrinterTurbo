# 第 4 阶段封面方案 Contract

本文件记录 TwinkleBite AI 餐饮宣传视频第 4 阶段封面生成模块的第一版 contract。

当前阶段只生成 `cover_plan.json`，用于描述封面应如何选择标题、图片、文案和布局。当前不渲染真实封面图片，不输出 PNG / JPG / JPEG / WebP 文件。

## 当前范围

- 根据用户输入的 `theme_text` 本地生成 3 个标题候选。
- 支持用户通过 `selected_cover_title_id` 或 `selected_cover_title` 选择标题。
- 将用户选择的标题写入 `selected_title`，并作为 `cover_copy.title`。
- 从用户上传图片中选择 1 张作为封面候选图。
- 只消费 `image_understanding` 和 `rule_engine_report` 的现有 contract。
- 输出仓库外样本目录中的 `output/cover_plan.json`。

当前不做：

- 不生成真实封面图片。
- 不调用 DeepSeek。
- 不调用任何外部 API。
- 不读取 API Key。
- 不读取图片像素。
- 不重新根据文件名分类。
- 不调用 TTS。
- 不生成音频。
- 不生成视频。
- 不修改 WebUI。

## Project 字段

`project.json` 可选新增字段：

```json
{
  "theme_text": "主打川菜，适合朋友聚餐，环境热闹，有招牌烤鱼和小龙虾。",
  "selected_cover_title_id": "title_1",
  "selected_cover_title": "朋友聚餐就来这家川味小馆",
  "selected_cover_image_id": "image_001"
}
```

字段说明：

- `theme_text`：用户输入的主题文案，用于本地静态标题候选生成。
- `selected_cover_title_id`：用户选择的标题 ID，优先级最高。
- `selected_cover_title`：用户选择的标题文本，仅在匹配候选标题文本时生效。
- `selected_cover_image_id`：用户指定的封面图片 ID，可使用 `image_001` 或数字形式。

兼容字段：

- `topic_text`
- `brief`
- `description`

当 `theme_text` 缺失时，上述字段可作为 fallback。

## 标题候选

当前标题 provider 固定为：

```text
local_static
```

输出 3 个稳定候选：

- `title_1`
- `title_2`
- `title_3`

每个候选字段：

- `title_id`
- `text`
- `source`
- `selected`

如果 `theme_text` 存在，当前使用本地模板生成短标题；如果不存在，使用默认候选：

- 餐厅宣传视频
- 精选美食与空间展示
- 发现这家宝藏餐厅

## 标题选择规则

选择优先级：

1. `selected_cover_title_id` 匹配候选 `title_id` 时生效。
2. `selected_cover_title` 匹配候选 `text` 时生效。
3. 否则默认选择 `title_1`。

无效选择不会阻断 pipeline，会在 `warnings` 中记录 `INVALID_TITLE_SELECTION`，并默认选择 `title_1`。

默认选择时：

- `user_selected=false`
- `selection_source=default_first_candidate`
- `quality_flags.requires_human_review=true`

## 封面图片选择规则

封面图片必须来自用户上传图片，也就是来自 `image_understanding` / `rule_engine_report` 已知图片。

选择优先级：

1. 有效的 `selected_cover_image_id`
2. `rule_engine_report.storyboard_hints.preferred_opening_image_id`
3. `rule_engine_report.asset_groups.hero_candidates`
4. `rule_engine_report.asset_groups.dish_candidates`
5. `rule_engine_report.asset_groups.interior_candidates`
6. `rule_engine_report.asset_groups.fallback_candidates`
7. `image_understanding.images` 第一张

如果没有任何图片：

- `primary_image_id=null`
- `has_primary_image=false`
- `blocking=true`

## cover_plan.json 顶层字段

`cover_plan.json` 顶层字段：

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

当前固定值：

- `planner=local_static`
- `external_api_called=false`
- `render_status=not_rendered`
- `cover_image_path=null`
- `quality_flags.requires_human_review=true`

## source_contracts

字段：

- `image_understanding_provider`
- `image_understanding_analysis_source`
- `rule_engine_version`
- `rule_engine`

该字段用于明确 cover planner 只消费第 3 阶段冻结 contract。

## title_generation

字段：

- `theme_text`
- `title_provider`
- `external_api_called`

当前：

- `title_provider=local_static`
- `external_api_called=false`

## selected_title

字段：

- `title_id`
- `text`
- `user_selected`
- `selection_source`

`cover_copy.title` 必须等于 `selected_title.text`。

## selected_assets

字段：

- `primary_image_id`
- `primary_image_path`
- `primary_asset_group`
- `selection_reason`
- `user_selected_image`
- `fallback_used`

## cover_copy

字段：

- `title`
- `subtitle`
- `cta`
- `language`
- `copy_source`

当前：

- `title` 来自 `selected_title.text`
- `copy_source=selected_title`

## layout

字段：

- `format`
- `safe_area`
- `text_zones`

当前 layout 仅为后续真实封面渲染提供占位 contract，不生成图片。

## quality_flags

字段：

- `requires_human_review`
- `content_based_understanding`
- `uses_filename_fallback`
- `has_primary_image`
- `has_user_selected_title`

当前即使 pipeline 成功，也默认 `requires_human_review=true`，因为第 4 阶段尚未接入真实视觉理解和封面渲染。

## pipeline_report 字段

`pipeline_report.json` 新增 cover 摘要字段：

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

## 安全边界

- 默认不调用任何外部 API。
- cover planner 不读取 API Key。
- cover planner 不读取图片像素。
- cover planner 不重新根据文件名分类。
- cover planner 不生成真实封面图片。
- `cover_image_path` 当前必须为空。
- `render_status` 当前必须为 `not_rendered`。
- storyboard 当前不强制消费 `cover_plan.json`。

## 后续阶段

后续可继续推进：

- 封面真实渲染 contract。
- 用户确认标题和封面图片的正式输入方式。
- 真实图片内容理解接入后降低人工复核风险。
- 视觉风格模板与封面图片生成。
