# restaurant_engine Pipeline 骨架说明

本文件记录第 2 阶段 `restaurant_engine` Pipeline 骨架。当前阶段只做本地项目读取、校验、图片扫描和 mock storyboard 输出，不生成真实视频。

## 当前目标

- 读取仓库外的餐厅样本 `project.json`。
- 调用已有 `restaurant_engine.validator.validate_project(...)` 校验输入。
- 根据 `project.json` 中的 `image_dir` 扫描本地图片。
- 在样本项目目录下创建 `output/`。
- 输出 mock 版 `storyboard.json`。
- 输出 `pipeline_report.json`。

## 输入与输出

示例输入：

```text
/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/project.json
```

示例输出：

```text
/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/output/image_understanding.json
/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/output/storyboard.json
/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/output/narration_plan.json
/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/output/pipeline_report.json
```

## Mock Image Understanding

pipeline 在 validator 通过并完成本地图片扫描后，会先生成本地 mock 版 `image_understanding.json`，再进入 storyboard planning。

当前阶段的 image understanding 只基于文件名规则：

- 不调用视觉模型。
- 不调用 OCR。
- 不调用 DeepSeek。
- 不调用任何外部 API。
- 不读取图片像素内容。

输出用途：

- 记录每张图片的 mock 类型识别。
- 记录是否允许进入视频。
- 记录适合封面、视频场景、辅助素材或需要人工复核。
- 为后续真实图片理解、图片筛选、封面选择和图生视频前置门禁保留 contract。

当前拒绝规则：

- 文件名包含 `qrcode` / `qr` / `phone` / `tel` / `address` / `menu` / `price` / `contact` / `wechat` / `wx` 时标记为 `invalid_*` 并拒绝进入视频。
- 拒绝图片当前只产生 warning，不阻塞 pipeline。
- 没有图片时为 error，pipeline `ok=false`。

`pipeline_report.json` 记录：

- `image_understanding_path`
- `image_understanding_passed`
- `allowed_image_count`
- `rejected_image_count`
- `image_category_counts`

详细字段和规则见 `restaurant_docs/IMAGE_UNDERSTANDING_SPEC.md`。

## Mock Storyboard 规则

- 每张图片生成一个 mock scene。
- 图片按文件名自然排序。
- scene 时长由 `target_duration_seconds` 和图片数量本地计算，全部为整数秒。
- scene 时长总和必须等于目标时长。
- 如果 `project.json` 缺少 `target_duration_seconds`，沿用 validator 默认值 `30` 秒。
- 当前整数秒分配示例：
  - `30 秒 / 8 图`：`4, 4, 3, 4, 4, 3, 4, 4`
  - `30 秒 / 6 图`：`5, 5, 5, 5, 5, 5`
  - `40 秒 / 8 图`：`5, 5, 5, 5, 5, 5, 5, 5`
  - `50 秒 / 10 图`：`5, 5, 5, 5, 5, 5, 5, 5, 5, 5`
  - `60 秒 / 12 图`：`5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5`
- 根据文件名识别基础角色：
  - `intro` / `storefront`：门头或开场。
  - `interior`：环境。
  - `dish_1` / `dish_2` / `dish_3`：菜品。
  - `dining` / `gathering`：用餐场景。
  - `detail`：细节。
  - `extra`：额外亮点。
  - 未识别时为 `unknown`。
- `mock_narration` 只用于占位，不调用 AI。

## Storyboard 时长对齐

当前 pipeline 在本地统一计算 scene 时长，不信任外部 planner 返回的时长字段：

- `compute_scene_durations(target_duration_seconds, image_count)` 返回整数秒列表。
- 返回列表长度等于图片数量。
- 返回列表总和等于目标时长。
- mock planner 直接使用该时长列表。
- DeepSeek planner prompt 中会写入目标时长、图片数量和要求的时长列表。
- DeepSeek 返回后仍由本地代码覆盖所有 scene 的 `duration_seconds`。
- DeepSeek scene 数量不匹配会失败。
- DeepSeek scene 顺序不匹配会失败。
- DeepSeek duration 不匹配不会失败，统一由本地时长列表归一化。

## Storyboard Contract 校验

pipeline 在生成 storyboard 后、写入 `storyboard.json` 前执行 contract 校验。该校验是后续进入 TTS、图生视频和视频合成前的结构门禁。

校验内容：

- `scenes` 必须存在且是数组。
- scene 数量必须等于本地图片数量。
- scene 的 `image_name` 顺序必须与图片文件名自然排序一致。
- 每个 scene 必须包含：
  - `index`
  - `role`
  - `image_name`
  - `image_path`
  - `duration_seconds`
  - `narration` 或 `mock_narration`
- `index` 必须从 `1` 开始连续递增。
- `image_path` 必须是字符串，且文件名与 `image_name` 一致。
- `duration_seconds` 必须是正整数。
- scene duration 总和必须等于 `target_duration_seconds`。
- `storyboard.total_duration_seconds` 必须等于 `target_duration_seconds`。
- `project_id` 和 `version` 必须存在。
- narration 文本不能为空。
- mock planner 中出现 mock 占位文案时记为 warning。
- DeepSeek planner 中出现 mock 占位文案时记为 error。

`pipeline_report.json` 记录：

- `storyboard_contract_passed`
- `storyboard_contract_errors`
- `storyboard_contract_warnings`
- `duration_sum`

如果 contract 校验失败：

- `validate_storyboard_contract` step 标记为 failed。
- `pipeline_report.ok=false`。
- pipeline 仍尽量写入 `pipeline_report.json`，方便定位问题。

## Storyboard Quality Contract 校验

结构 contract 通过后，pipeline 会继续执行 storyboard quality contract。该校验关注 storyboard 是否可用于餐厅宣传片后续链路，而不仅是 JSON 结构正确。

质量校验内容：

- narration 不能为空。
- narration 必须包含中文宣传文案。
- narration 中文字符数不能过短或过长。
- scene narration 不能重复。
- scene 必须包含非空：
  - `visual_instruction`
  - `selling_point`
  - `transition_hint`
- 不允许出现明显占位或 mock 文案，例如 `Mock narration`、`mock storyboard only`、`TODO`、`待填写`、`占位`。
- DeepSeek planner 中出现 mock / placeholder 文案会作为 error。
- mock planner 也必须输出结构完整、可读的中文占位 storyboard，而不是简单英文 mock 文案。

`pipeline_report.json` 记录：

- `storyboard_quality_passed`
- `storyboard_quality_errors`
- `storyboard_quality_warnings`

如果 quality contract 失败：

- `validate_storyboard_quality` step 标记为 failed。
- `pipeline_report.ok=false`。
- pipeline 仍尽量写入 `pipeline_report.json`，方便定位问题。

## Planner 模式

当前 pipeline 支持两个 planner：

- `mock`：默认模式，只生成本地 mock storyboard，不调用外部 API。
- `deepseek`：DeepSeek storyboard planner，需要显式允许外部 API。

默认 planner 仍为 `mock`。普通 pipeline 验证不应触发外部 API。

默认命令等价于 `--planner mock`：

```bash
python3 -m restaurant_engine.pipeline_project \
  --project /Users/feei/AI/restaurant-video-ai-samples/sichuan_001/project.json
```

DeepSeek 必须同时提供：

```bash
python3 -m restaurant_engine.pipeline_project \
  --project /Users/feei/AI/restaurant-video-ai-samples/sichuan_001/project.json \
  --planner deepseek \
  --allow-external-api
```

当前 DeepSeek 真实调用已通过首次 smoke test：

- DeepSeek planner 已能输出真实 `storyboard.json`。
- `pipeline_report.ok=true`。
- `planner=deepseek`。
- `external_api_allowed=true`。
- `external_api_called=true`。
- scene 数量与图片数量一致。
- scene 顺序与图片顺序一致。
- 未发现 API Key、请求头或 token 写入 report/storyboard。

DeepSeek planner 真实时长对齐测试也已通过：

- DeepSeek 返回的 duration 不再作为最终时长来源。
- 最终 scene duration 由本地 `compute_scene_durations(...)` 根据 `target_duration_seconds` 和 `image_count` 强制生成。
- 当前验证样例：
  - `target_duration_seconds=30`
  - `image_count=8`
  - `scene_durations=[4, 4, 3, 4, 4, 3, 4, 4]`
  - `total_duration_seconds=30`
- 真实 DeepSeek 返回后，storyboard 中的 scene duration 已按本地规则归一化。
- 当前仍不生成视频、不调用 TTS、不调用图生视频。

如果只传 `--planner deepseek` 但没有 `--allow-external-api`：

- 不调用 DeepSeek。
- `pipeline_report.json` 写入 `ok=false`。
- `external_api_called=false`。
- CLI 返回非 0。

## DeepSeek 安全边界

- API Key 优先来自环境变量 `DEEPSEEK_API_KEY`。
- 如果环境变量不存在，再从本地 `config.toml` 的 `deepseek_api_key` 读取。
- Base URL 优先来自 `DEEPSEEK_BASE_URL`，再读本地配置，最后 fallback 到 `https://api.deepseek.com/v1`。
- Model 优先来自 `DEEPSEEK_MODEL`，再读本地配置，最后 fallback 到 `deepseek-chat`。
- `config.toml` 不进入 Git。
- 不把 API Key 写入 `pipeline_report.json`、`storyboard.json` 或日志。
- 不把完整请求头写入 report。
- 不建议把完整 prompt/response 写入 report。
- 默认 mock 模式不读取 DeepSeek key，也不调用外部 API。

## 当前不做

- 不生成视频。
- 不生成封面。
- 默认不调用 DeepSeek；真实调用必须显式 `--planner deepseek --allow-external-api`。
- 不调用 TTS。
- 不调用 AI 图生视频。
- 不接真实图生视频服务商。
- 不调用外部 API。
- 不修改 MoneyPrinterTurbo WebUI。
- 不修改 MoneyPrinterTurbo 视频生成核心。

## CLI

支持两种调用方式：

```bash
python3 -m restaurant_engine.pipeline_project \
  /Users/feei/AI/restaurant-video-ai-samples/sichuan_001/project.json

python3 -m restaurant_engine.pipeline_project \
  --project /Users/feei/AI/restaurant-video-ai-samples/sichuan_001/project.json
```

CLI 输出：

- `project_id`
- `ok`
- `validation_passed`
- `image_count`
- `output_dir`
- `storyboard`
- `pipeline_report`
- `issues`

## 输出结构

`storyboard.json` 包含：

- `project_id`
- `version`
- `scenes`
- `total_duration_seconds`
- `total_mock_duration_seconds`
- `notes`

`pipeline_report.json` 包含：

- `ok`
- `project_id`
- `project_json_path`
- `image_dir`
- `output_dir`
- `image_count`
- `image_understanding_path`
- `image_understanding_passed`
- `allowed_image_count`
- `rejected_image_count`
- `image_category_counts`
- `storyboard_path`
- `narration_plan_path`
- `validation_passed`
- `target_duration_seconds`
- `scene_count`
- `scene_durations`
- `total_duration_seconds`
- `duration_normalized`
- `steps`
- `issues`

## 后续阶段

- 将 mock storyboard 替换为可配置的脚本/分镜规划。
- 接入真实文案生成，但仍保持可测试的本地报告输出。
- 接入 TTS 前先冻结输入/输出契约。
- 接入视频生成前保留 dry-run / mock 模式。
- 继续增强 DeepSeek prompt 的文案节奏和结构约束。
- 增加更严格的 storyboard schema 校验。
- 增加 DeepSeek 输出质量评分。
- 在 TTS / 视频链路接入前补充 contract 检查。

## Storyboard Quality Contract 阈值

当前 quality contract 用于在进入 TTS、图生视频和视频合成前拦截不可用 storyboard 内容。

硬性 error：

- narration 为空。
- narration 不包含中文字符，错误码为 `non_chinese_narration`。
- narration 少于 4 个中文字符，错误码为 `narration_too_short_hard`。
- narration 超过最大建议长度。
- scene narration 重复。
- `visual_instruction`、`selling_point`、`transition_hint` 缺失或为空。
- DeepSeek planner 返回 mock、placeholder、TODO、待填写等占位内容。

warning：

- narration 有 4 到 7 个中文字符时，记录 `narration_too_short` warning。
- 该区间的短促中文宣传句可以通过 quality contract，例如“正宗川味，太上头！”。
- `visual_instruction` 过短或餐厅宣传信号偏弱时记录 warning。

DeepSeek planner prompt 约束：

- narration 应为自然中文短句，优先不少于 8 个中文字符。
- 不返回过短片段。
- 不返回 mock、placeholder、TODO、待填写或 Markdown。
- scene 数量和图片顺序必须保持输入顺序。
- duration 由本地 `compute_scene_durations` 归一化，DeepSeek 返回值不作为最终时长来源。

## DeepSeek Quality Contract 真实复测

- DeepSeek storyboard quality contract 真实复测已通过。
- 当前 DeepSeek planner 输出在真实 API 调用后可通过：
  - structure contract
  - quality contract
  - duration alignment
  - image order check
- quality warning 不阻断 pipeline。
- quality error 才阻断 pipeline。
- 当前验证样例：
  - `target_duration_seconds=30`
  - `image_count=8`
  - `scene_durations=[4,4,3,4,4,3,4,4]`
  - `total_duration_seconds=30`
  - `quality_errors=0`
  - `quality_warnings=3`
- 当前仍不生成视频、不调用 TTS、不调用图生视频。
- 后续可进入：
  - TTS contract 设计
  - storyboard-to-narration 导出
  - 图生视频适配层设计
  - 新项目 `restaurant-video-ai` 架构设计

## Narration Plan / TTS Contract 骨架

在接入真实 TTS 前，pipeline 先从已通过 storyboard structure / quality contract 的 storyboard 生成本地 `narration_plan.json`。

输出文件：

- `storyboard.json`
- `narration_plan.json`
- `pipeline_report.json`

`narration_plan.json` 当前包含：

- `project_id`
- `version`
- `lines`
- `target_duration_seconds`
- `total_scene_duration_seconds`
- `total_duration_seconds`
- `total_estimated_speech_seconds`
- `speech_rate_cjk_per_second`
- `notes`

每条 `lines` 包含：

- `scene_index`
- `image_name`
- `duration_seconds`
- `narration`
- `cjk_char_count`
- `estimated_tts_seconds`
- `estimated_speech_seconds`
- `recommended_max_cjk_chars`

TTS contract 当前规则：

- narration 为空：error。
- narration 不含中文：error。
- `duration_seconds <= 0`：error。
- 估算朗读时长超过 scene 时长：warning。
- 估算朗读时长超过 scene 时长 3 秒以上：error。

当前阶段边界：

- 不生成音频。
- 不调用 TTS。
- 不调用 DeepSeek。
- 不调用任何外部 API。
- 不生成视频。
- 不修改 WebUI、`app/` 或 `config.toml`。

## DeepSeek Narration Plan / TTS Contract 真实复测

- DeepSeek narration plan / TTS contract 真实复测已通过。
- 当前 DeepSeek planner 输出在真实 API 调用后可通过：
  - storyboard structure contract
  - storyboard quality contract
  - duration alignment
  - `narration_plan` 生成
  - TTS contract
- TTS contract warning 不阻断 pipeline。
- TTS contract error 才阻断 pipeline。
- 当前验证样例：
  - `target_duration_seconds=30`
  - `image_count=8`
  - `scene_durations=[4,4,3,4,4,3,4,4]`
  - `total_duration_seconds=30`
  - `narration_line_count=8`
  - `estimated_total_tts_seconds=32.0`
  - `tts_errors=0`
  - `tts_warnings=5`
- 当前仍不调用真实 TTS、不生成音频、不生成视频。
- 后续可进入：
  - 真实 TTS 接入设计
  - audio duration 校准
  - per-scene audio 输出 contract
  - 图生视频适配层设计
