# 第 4 阶段验收：封面生成模块 Contract Freeze

本文件记录餐饮 AI 宣传视频生成系统第 4 阶段“封面生成模块”的最终验收边界。第 4 阶段产物用于支撑 MoneyPrinterTurbo 验证仓库中的封面生成 prototype，并作为第 5 阶段“分镜脚本与口播文案生成”的输入 contract。

## A. 阶段范围

第 4 阶段已完成：

- 封面标题后台生成。
- 本地标题质量规则。
- `cover_prompt` 生成。
- 视频比例接入。
- RunningHub batch provider。
- WebUI 生成 3 张封面并展示。
- 用户选择 1 张封面。
- fake RunningHub / AppTest 验证。
- 缺配置受控失败。
- RunningHub 真实 output parser 修复。
- 使用已提交真实 task 恢复下载 3 张结果图。
- 早期 `cover_plan.json` / `cover_render_report.json` / local Pillow renderer contract 保留为历史验证能力。

第 4 阶段不包含：

- 第 5 阶段正式分镜脚本升级。
- 正式口播文案生成。
- TTS。
- 音频生成。
- 视频生成。
- 图生视频。
- 最终 Web 产品。
- 用户系统。
- 支付。
- 部署。

## B. 已完成提交

- `d517160 feat: add local cover plan contract`
- `7bea98d feat: add local cover renderer`
- `9c00e82 chore: freeze stage 4 contracts`
- `a7ba09d feat: add restaurant cover webui prototype`
- `142c8c9 fix: move cover generation button to video settings`
- `16c6261 fix: keep restaurant cover script generation local`
- `2aa4818 feat: add runninghub cover batch prototype`
- `7a18109 feat: add runninghub cover prompts and ratio support`
- `151859c fix: handle runninghub output parsing`

## C. WebUI Contract

- 文案设置区域的 AI 视频文案按钮只生成视频文案。
- WebUI 不展示标题候选。
- WebUI 不提供标题选择 UI。
- 标题只在点击 `生成封面` / `重新生成封面` 时后台生成。
- 图片数量小于 3 张时，生成封面按钮不可点击或显示受控提示。
- 图片数量达到 3 张后，生成封面按钮可点击。
- 生成封面按钮位于中间列 `视频设置` 区域。
- 生成封面按钮位于 `当前本地图片数量：X 张` 下方。
- 生成期间显示 loading：`正在生成 3 张封面，请稍候...`。
- 成功后展示 3 张封面。
- 用户可选择 1 张封面。
- 选中封面有高亮 / 描边状态。
- 重新生成会刷新 batch，包括标题批次、随机图片和 3 张封面。

WebUI 选择状态写入 session state：

- `selected_cover_variant_id`
- `selected_cover_image_path`
- `selected_cover_title_text`
- `selected_cover_source_image_path`

## D. RunningHub Provider Contract

- `provider=runninghub`
- `workflow_provider=runninghub`
- workflow URL：`https://www.runninghub.cn/workflow/2064397787445424129`
- workflow ID：`2064397787445424129`
- node mapping：
  - image input：`13.image`
  - prompt input：`3.prompt`
  - output：`4.images`

必需环境变量：

- `RUNNINGHUB_API_KEY`
- `RUNNINGHUB_COVER_WORKFLOW_ID`
- `RUNNINGHUB_COVER_IMAGE_NODE_ID`
- `RUNNINGHUB_COVER_TITLE_NODE_ID`

建议环境变量：

- `RUNNINGHUB_COVER_IMAGE_NODE_FIELD`
- `RUNNINGHUB_COVER_TITLE_NODE_FIELD`
- `RUNNINGHUB_COVER_OUTPUT_NODE_ID`
- `RUNNINGHUB_COVER_OUTPUT_NODE_FIELD`

可选环境变量：

- `RUNNINGHUB_COVER_RATIO_NODE_ID`
- `RUNNINGHUB_COVER_RATIO_NODE_FIELD`
- `RUNNINGHUB_COVER_RATIO_16_9_VALUE`
- `RUNNINGHUB_COVER_RATIO_9_16_VALUE`
- `RUNNINGHUB_COVER_NODE_INFO_JSON`
- `RUNNINGHUB_API_BASE`
- `RUNNINGHUB_POLL_INTERVAL_SECONDS`
- `RUNNINGHUB_TIMEOUT_SECONDS`
- `RUNNINGHUB_COVER_UPLOAD_ENDPOINT`
- `RUNNINGHUB_COVER_CREATE_ENDPOINT`
- `RUNNINGHUB_COVER_STATUS_ENDPOINT`
- `RUNNINGHUB_COVER_OUTPUTS_ENDPOINT`

缺配置行为：

- 受控失败。
- 不调用 RunningHub。
- 不 fallback 到 fake client。
- 不 fallback 到 local Pillow。
- 不调用 DeepSeek / LLM。
- 不输出 API Key。
- 不记录敏感 signed URL。

## E. Title Contract

- 标题后台生成。
- WebUI 不展示标题候选。
- 标题 provider 为 `local_static`。
- 每批 3 条标题。
- `batch_index` 可刷新标题批次。
- 标题质量规则建议 6–16 个中文字符。

禁用弱模板：

- `值得一试`
- `聚餐首选`
- `发现这家`
- `必吃`
- `宝藏`
- `绝了`

禁止夸张承诺：

- `全城第一`
- `天花板`
- `全网爆火`
- `100% 好吃`
- `不吃后悔`

## F. Cover Prompt Contract

- 每个 RunningHub task 都有 `cover_prompt`。
- `cover_prompt` 包含：
  - 风格要求。
  - 标题文字。
  - 比例。
- RunningHub `3.prompt` 节点接收完整 `cover_prompt`。
- 不提交裸标题。
- 不使用 LLM 生成 prompt。
- prompt 要求避免多余小字、二维码、电话、价格和夸张营销词。

## G. Aspect Ratio Contract

- 支持 `9:16`。
- 支持 `16:9`。
- 比例来自 WebUI 现有 `视频比例` 字段。
- prompt 中必须包含比例。
- ratio node 是可选配置。
- 如果配置 `RUNNINGHUB_COVER_RATIO_NODE_ID` 和 `RUNNINGHUB_COVER_RATIO_NODE_FIELD`，provider 会提交独立比例节点。
- 未配置 ratio node 时，不阻塞任务，比例写入 prompt，并记录：
  - `RATIO_NODE_NOT_CONFIGURED_PROMPT_ONLY`

## H. cover_batch_report Contract

顶层字段至少包括：

- `version`
- `provider`
- `workflow_provider`
- `workflow_id`
- `image_node_id`
- `image_node_field`
- `title_node_id`
- `title_node_field`
- `output_node_id`
- `output_node_field`
- `external_api_called`
- `batch_index`
- `theme_text`
- `aspect_ratio`
- `prompt_style_version`
- `title_quality_version`
- `min_required_images`
- `uploaded_image_count`
- `selected_cover_variant_id`
- `variants`
- `warnings`
- `blocking`
- `cover_batch_report_path`

`variants[]` 至少包括：

- `variant_id`
- `title_id`
- `title_text`
- `title_source`
- `title_quality_passed`
- `title_quality_warnings`
- `cover_prompt`
- `prompt_source`
- `aspect_ratio`
- `source_image_path`
- `source_image_name`
- `runninghub_task_id`
- `runninghub_status`
- `remote_result_ref` 或脱敏 URL
- `remote_result_url`
- `local_cover_image_path`
- `render_status`
- `output_width`
- `output_height`
- `external_api_called`
- `warnings`

安全要求：

- report 不得写入 API Key。
- report 不得写入 Authorization header。
- report 不得写入 Bearer token。
- report 不得写入敏感 signed query。

## I. 测试结果

- fake RunningHub AppTest：通过。
- `9:16` payload：通过。
- `16:9` payload：通过。
- 缺配置测试：通过。
- parser fake response tests：通过。
- RunningHub 真实 task 恢复：通过。
- 3 个真实 task 均为 `succeeded`：
  - `2064568458020081665`
  - `2064568466555494401`
  - `2064568474776334338`
- 3 张真实图片已下载到 `/private/tmp`。
- 真实图片尺寸：`943 x 1668`。
- 未提交新 RunningHub task。
- 未产生仓库内 output。
- 未调用 DeepSeek / LLM / TTS。
- 未生成音频或视频。

## J. 第 5 阶段可依赖字段

第 5 阶段可以依赖：

- `cover_batch_report.variants[*].title_text`
- `cover_batch_report.variants[*].cover_prompt`
- `cover_batch_report.variants[*].aspect_ratio`
- `cover_batch_report.variants[*].local_cover_image_path`
- `cover_batch_report.variants[*].render_status`
- `cover_batch_report.selected_cover_variant_id`
- pipeline / WebUI 记录的 selected cover 信息。
- WebUI 当前视频文案文本。
- 用户上传图片列表。
- 视频比例字段。
- 早期本地 contract 中的 `cover_plan.selected_title.text`。
- 早期本地 contract 中的 `cover_render_report.cover_image_path`。

## K. 第 5 阶段不得假设

第 5 阶段不得假设：

- 可以调用 DeepSeek。
- 可以调用 LLM。
- 可以调用 TTS。
- 可以生成音频。
- 可以生成视频。
- 可以直接进入正式产品。
- cover image 一定是 `1080 x 1920`。
- RunningHub 真实输出尺寸固定。
- `filename_fallback` 是正式视觉理解。
- 已经接入真实视觉模型。
- WebUI 是最终产品。
- RunningHub 每次都一定返回 3 张可用图片。
- RunningHub URL / output schema 永远不变。

## 已知限制

- WebUI 仍是 MoneyPrinterTurbo 验证仓库中的临时 prototype，不是最终产品。
- RunningHub 真实输出尺寸目前观测为 `943 x 1668`，不是固定 contract。
- 标题仍为本地 `local_static`，不是真实营销标题模型。
- 图片理解仍未接入真实视觉模型。
- 第 4 阶段不生成音频或视频。
- 真实 RunningHub 调用需要用户显式配置环境变量并授权。

## 是否可以进入第 5 阶段

可以进入第 5 阶段准备，但第 5 阶段必须继续遵守：

- 默认不调用外部 API。
- 不默认调用 DeepSeek / LLM / TTS。
- 不把 WebUI prototype 当最终产品。
- 使用第 4 阶段冻结的 `cover_batch_report` / selected cover 字段作为输入 contract。
