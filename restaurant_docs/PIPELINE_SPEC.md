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
/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/output/storyboard.json
/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/output/pipeline_report.json
```

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
- `storyboard_path`
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
