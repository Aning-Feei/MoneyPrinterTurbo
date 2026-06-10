# 第 4 阶段 WebUI 临时封面验证入口

本文件记录 MoneyPrinterTurbo WebUI 中新增的餐饮封面生成临时验证入口。

该入口只用于第 4 阶段封面生成模块的本地验证，不是第 9 阶段正式 Web 产品，也不是后续 `restaurant-video-ai` 正式项目。

最新交互修正：

- 标题/文案生成动作已并入现有 WebUI 左侧 `文案设置` 区域。
- `文案设置` 中按钮显示为 `生成视频文案`，只生成本地 prototype 视频文案。
- 前台不再展示标题候选，也不提供标题选择控件。
- 标题只在点击 `生成封面` / `重新生成封面` 时后台本地生成，每批 3 条。
- `生成封面` 按钮移动到中间列 `视频设置` 区域，位于 `当前本地图片数量` 下方。
- 封面生成复用视频设置中的本地上传图片，不再提供独立图片上传入口。
- 上传图片达到 3 张后，WebUI 随机选择 3 张图片，与 3 条标题一一配对，提交 RunningHub batch。

## 当前目标

- 用户输入视频主题，内部写入 `theme_text`。
- 用户点击 `生成视频文案`。
- WebUI 本地生成 prototype 视频文案。
- 用户在 `视频设置` 中上传至少 3 张餐厅图片。
- WebUI 点击 `生成封面` 时后台生成 3 条 `local_static` 高吸引力标题。
- WebUI 随机选择 3 张图片，提交 3 个 RunningHub 封面任务。
- RunningHub 返回 3 张封面后，WebUI 展示并允许用户选择其中 1 张。
- 展示 `cover_batch_report` 的必要摘要。

## 复用模块

WebUI 不调用 DeepSeek、LLM 或 TTS。当前封面 batch provider 为：

- `restaurant_engine.cover_planner.build_title_candidates`
- `restaurant_engine.runninghub_cover.generate_runninghub_cover_batch`

标题候选仍由 `cover_planner` 本地静态逻辑生成：

- `title_1`
- `title_2`
- `title_3`

标题 `source` 固定为：

```text
local_static
```

标题模板已做第 4 阶段质量修正：

- 不再使用 `值得一试`、`聚餐首选`、`发现这家` 作为主要标题后缀。
- 不再使用 `不容错过`、`强烈推荐`、`必吃`、`宝藏`、`绝了` 等弱模板。
- 不使用 `全城第一`、`天花板`、`史上最强`、`全网爆火`、`100% 好吃`、`不吃后悔` 等夸张承诺。
- 不再简单拼接 `主题 + 后缀`。
- 当前按本地规则生成更适合短视频封面主标题的 3 个角度：
  - 味道钩子
  - 场景钩子
  - 氛围/发现感钩子
- 标题质量规则版本：`cover-title-quality-v1`，建议 6–16 个中文字符。
- 仍为 deterministic 本地模板，不调用 DeepSeek、LLM 或外部 API。

RunningHub 接入时不再把裸标题直接提交给 prompt 节点，而是本地生成完整 `cover_prompt`：

- 包含主题、标题文字、视频比例和封面风格要求。
- prompt 风格版本：`cover-prompt-style-v1`。
- 示例标题：`这锅川味越吃越上头`。
- 示例比例：`9:16`。
- prompt 中包含：`文字：“这锅川味越吃越上头”`、`比例：9:16`。

视频文案当前由 WebUI 本地 prototype 逻辑生成，仅作为 WebUI 临时验证入口的本地文案展示，不调用 DeepSeek、LLM 或外部 API。

## 临时目录

上传图片和 pipeline 输出写入仓库外临时目录：

```text
/private/tmp/mpt-restaurant-webui/
```

每次生成封面会创建独立 run 目录，包含：

- `images/`
- `output/cover_1.png`
- `output/cover_2.png`
- `output/cover_3.png`
- `output/cover_batch_report.json`

这些文件不得提交 Git。

## UI 行为

- `生成视频标题` 按钮位于左侧 `文案设置` 区域的目标时长说明下方。
- 点击 `生成视频标题` 后，本地生成 6 条 `local_static` 视频标题。
- 6 条标题展示在标题按钮下方，用户必须选择其中 1 条，默认选中 `title_1`。
- `生成视频文案` 按钮只生成 prototype 视频文案，并写入现有 `视频文案` 输入框。
- `生成视频文案` 不刷新标题列表，不覆盖已选标题。
- prototype 视频文案按目标时长中文字符范围生成。
- 标题选择写入 session state：`selected_video_title_id` / `selected_video_title_text`。
- 封面生成读取现有 `视频比例` 设置，只支持 `9:16` 和 `16:9`。
- 封面验证入口位于中间列 `视频设置` 区域的 `当前本地图片数量` 下方。
- 上传图片少于 3 张时，WebUI 提示 `至少上传 3 张图片后可生成封面。`，按钮不可点击。
- 上传图片达到 3 张后，按钮显示 `生成封面`；成功生成后显示 `重新生成封面`。
- 点击生成封面前必须已经选择视频标题；未选择时受控提示，不调用 RunningHub。
- 点击生成封面后，WebUI 随机选择 3 张用户上传图片，并用同一条用户选择标题提交 3 个 RunningHub 任务。
- 生成期间封面结果区域显示 `正在生成 3 张封面，请稍候...`。
- 成功后展示 3 张 RunningHub 封面图，用户可选择其中 1 张，选中项有高亮样式。
- 结果区展示封面编号、预览图、选中状态、比例、渲染状态和必要 warning。
- 选择结果写入 session state：`selected_cover_variant_id` / `selected_cover_image_path` / `selected_cover_title_text` / `selected_cover_source_image_path` / `selected_cover_aspect_ratio`。

## 安全边界

当前入口：

- 不调用 DeepSeek。
- 不调用非 RunningHub 外部 API。
- 不调用 LLM。
- 不读取 API Key。
- 不调用视觉模型。
- 真实 RunningHub 封面生成只在用户配置环境变量并点击生成封面时执行。
- 不调用 TTS。
- 不生成音频。
- 不生成视频。
- 不修改 MoneyPrinterTurbo 原有视频生成主链路。
- 不写入 `storage/`。
- 不写入 `resource/`。
- 不写入仓库源码目录的 output。

## RunningHub 输出解析边界

- WebUI 依赖 `restaurant_engine.runninghub_cover` 返回的 `cover_batch_report.json`。
- provider 需要兼容真实 RunningHub status / outputs 中的 string、dict、list 和 nested dict 结构。
- 如果真实 task 失败或输出结构未知，WebUI 展示受控 warning，不展示 Python traceback。
- `remote_result_url` 只允许保存脱敏 URL，不得展示或写入敏感 signed query。
- 修复 parser 后，可使用已提交 task id 查询输出；不得把该查询视为新的封面生成任务。

## 当前边界

- 这是临时 prototype / validation 入口。
- 不是最终产品 UI。
- 不进入第 5 阶段。
- 图片理解默认使用 `mock` provider，不读取图片语义。
- 缺少 RunningHub 配置时受控失败，不 fallback 到本地 Pillow 假结果。

## 第 4 阶段最终验收状态

- WebUI 分别显示 `生成视频标题` 和 `生成视频文案`。
- 点击标题按钮时生成 6 条视频标题；点击文案按钮时只生成视频文案。
- WebUI 展示 6 条标题并允许用户选择 1 条作为封面主标题。
- 点击 `生成封面` / `重新生成封面` 时，3 个 RunningHub task 使用同一条用户选择标题。
- `生成封面` 位于中间列 `视频设置` 区域的 `当前本地图片数量：X 张` 下方。
- 图片数量小于 3 张时按钮不可点击或显示受控提示。
- 图片数量达到 3 张后可提交 RunningHub batch。
- 生成期间显示 loading。
- 成功后展示 3 张封面，用户可选择 1 张，选中项有高亮 / 描边。
- 选择信息写入 session state，供第 5 阶段继续消费。
- 第 4 阶段只冻结 prototype contract，不代表最终产品 UI。
