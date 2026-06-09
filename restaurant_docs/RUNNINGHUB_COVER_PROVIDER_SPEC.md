# RunningHub Cover Provider Prototype

本文件记录第 4 阶段 MoneyPrinterTurbo WebUI 临时验证入口的 RunningHub 封面生成 provider。

## 定位

- 当前仍属于第 4 阶段：封面生成模块。
- 当前是 MoneyPrinterTurbo WebUI 临时验证入口，不是最终 `restaurant-video-ai` 产品。
- 当前不进入第 5 阶段正式视频文案系统。
- 当前不调用 DeepSeek、不调用 LLM、不调用 TTS、不生成音频或视频。

## WebUI 流程

1. `文案设置` 中按钮显示为 `生成视频文案`，只生成本地 prototype 视频文案。
2. WebUI 不展示标题候选列表，也不提供标题选择控件。
3. 用户上传至少 3 张图片后，`生成封面` 按钮可点击。
4. 点击 `生成封面` 后，后台本地生成 3 条 `local_static` 标题。
5. 系统随机选择 3 张用户上传图片。
6. 系统提交 3 个 RunningHub 封面任务：
   - `title_1 + image_1`
   - `title_2 + image_2`
   - `title_3 + image_3`
7. RunningHub 返回 3 张封面图后，WebUI 展示 3 张封面。
8. 用户可选择其中 1 张封面，选中项会高亮并写入 session state。
9. 成功生成后按钮文案变为 `重新生成封面`，再次点击会刷新标题批次、随机图片和 3 张封面。

## Provider 文件

```text
restaurant_engine/runninghub_cover.py
```

职责：

- 读取 RunningHub 配置。
- 上传图片。
- 提交 workflow task。
- 轮询 / 查询任务结果。
- 下载生成图片。
- 输出 `cover_batch_report.json`。

## 参考 RunningHub Workflow

本轮校准参考用户本机下载的 RunningHub workflow API JSON：

```text
/Users/feei/Downloads/视频封面设计-全能图片G2图像编辑（RH版）_api.json
/Users/feei/Downloads/视频封面设计-全能图片G2图像编辑（RH版）.json
```

这两个文件只作为本机只读参考，不复制进仓库，不提交 Git。

参考 workflow：

```text
https://www.runninghub.cn/workflow/2064397787445424129
```

参考 workflow id：

```text
2064397787445424129
```

从 `_api.json` 读取到的非敏感节点摘要：

| 用途 | 节点 ID | 字段 | 节点类型/说明 |
|---|---:|---|---|
| 图片输入 | 13 | image | LoadImage |
| 标题/提示词输入 | 3 | prompt | CR Prompt Text |
| 封面生成 | 1 | prompt / image1 | RH_RhartImageG2ImageToImage |
| 输出保存 | 4 | images | SaveImage |

provider 不硬编码该 workflow id；真实运行时仍通过环境变量配置。

注意：下载的 `_api.json` 确认的是 workflow graph / node mapping，不包含完整 REST endpoint、task polling 和 result download 模板。因此 provider 继续保留 upload/create/status/outputs endpoint 环境变量，真实 smoke 前需要按 RunningHub 当前 OpenAPI 文档或用户账号实际接口确认。

## 环境变量

必需：

```text
RUNNINGHUB_API_KEY
RUNNINGHUB_COVER_WORKFLOW_ID
RUNNINGHUB_COVER_IMAGE_NODE_ID
RUNNINGHUB_COVER_TITLE_NODE_ID
```

可选：

```text
RUNNINGHUB_API_BASE
RUNNINGHUB_POLL_INTERVAL_SECONDS
RUNNINGHUB_TIMEOUT_SECONDS
RUNNINGHUB_COVER_IMAGE_NODE_FIELD
RUNNINGHUB_COVER_TITLE_NODE_FIELD
RUNNINGHUB_COVER_OUTPUT_NODE_ID
RUNNINGHUB_COVER_OUTPUT_NODE_FIELD
RUNNINGHUB_COVER_NODE_INFO_JSON
RUNNINGHUB_COVER_UPLOAD_ENDPOINT
RUNNINGHUB_COVER_CREATE_ENDPOINT
RUNNINGHUB_COVER_STATUS_ENDPOINT
RUNNINGHUB_COVER_OUTPUTS_ENDPOINT
```

当前参考 workflow 的建议配置：

```text
RUNNINGHUB_COVER_WORKFLOW_ID=2064397787445424129
RUNNINGHUB_COVER_IMAGE_NODE_ID=13
RUNNINGHUB_COVER_IMAGE_NODE_FIELD=image
RUNNINGHUB_COVER_TITLE_NODE_ID=3
RUNNINGHUB_COVER_TITLE_NODE_FIELD=prompt
RUNNINGHUB_COVER_OUTPUT_NODE_ID=4
RUNNINGHUB_COVER_OUTPUT_NODE_FIELD=images
```

`RUNNINGHUB_COVER_NODE_INFO_JSON` 可用于描述复杂 workflow node mapping，支持 `{{image}}` 和 `{{title}}` 占位符。脱敏示例：

```json
[
  {"nodeId": "13", "fieldName": "image", "fieldValue": "{{image}}"},
  {"nodeId": "3", "fieldName": "prompt", "fieldValue": "{{title}}"}
]
```

也可使用对象形式：

```json
{
  "nodeInfoList": [
    {"nodeId": "13", "fieldName": "image", "fieldValue": "{{image}}"},
    {"nodeId": "3", "fieldName": "prompt", "fieldValue": "{{title}}"}
  ]
}
```

文档不得写入 `RUNNINGHUB_API_KEY` 的值。

## 缺配置行为

- 缺少必需配置时，WebUI 显示受控提示：
  - `RunningHub 封面生成配置缺失，请配置 API Key 和 workflow 信息。`
- 不调用 RunningHub。
- 不 fallback 到 DeepSeek、LLM、AI 图片生成或本地 Pillow 假结果。

## 真实 Smoke 条件

真实 RunningHub smoke 必须由用户后续单独授权，并且满足：

- 已配置 `RUNNINGHUB_API_KEY`。
- 已配置 workflow id 和 image/title node mapping。
- 如 workflow 需要复杂 node mapping，已配置 `RUNNINGHUB_COVER_NODE_INFO_JSON`。
- 用户明确允许执行真实 RunningHub 外部 API 调用。

本轮只完成 workflow API JSON 校准，不执行真实 RunningHub 任务。

## 输出报告

每次 batch 输出到仓库外临时目录：

```text
/private/tmp/mpt-restaurant-webui/<session>/<run>/output/cover_batch_report.json
```

报告包含：

- `provider=runninghub`
- `workflow_provider=runninghub`
- `external_api_called=true`
- `batch_index`
- `theme_text`
- `min_required_images`
- `uploaded_image_count`
- `selected_cover_variant_id`
- `variants[]`
  - `variant_id`
  - `title_id`
  - `title_text`
  - `title_source`
  - `source_image_path`
  - `runninghub_task_id`
  - `runninghub_status`
  - `remote_result_ref`
  - `remote_result_url`
  - `local_cover_image_path`
  - `render_status`
  - `output_width`
  - `output_height`
  - `external_api_called`
- `warnings`
- `blocking`

报告不得写入 API Key、Authorization header、Bearer token 或敏感签名 URL。

## 当前边界

- RunningHub 是本阶段唯一允许的外部封面生成 provider。
- 本地 Pillow renderer 可保留为历史模块，但 WebUI `生成封面` 不使用 Pillow 结果冒充 RunningHub。
- Mock / fake client 只用于 AppTest，不作为缺配置 fallback。
- 当前不提交生成图片和 report。
