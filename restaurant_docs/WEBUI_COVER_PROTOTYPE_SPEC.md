# 第 4 阶段 WebUI 临时封面验证入口

本文件记录 MoneyPrinterTurbo WebUI 中新增的餐饮封面生成临时验证入口。

该入口只用于第 4 阶段封面生成模块的本地验证，不是第 9 阶段正式 Web 产品，也不是后续 `restaurant-video-ai` 正式项目。

最新交互修正：

- 标题/文案生成动作已并入现有 WebUI 左侧 `文案设置` 区域。
- `文案设置` 中原 AI 文案按钮显示为 `生成视频标题/视频文案`。
- 封面验证区不再提供独立主题输入或独立标题/文案生成按钮。
- 封面验证区只复用 `文案设置` 生成并选中的标题。
- `生成封面` 按钮移动到中间列 `视频设置` 区域，位于 `当前本地图片数量` 下方。
- 封面生成复用视频设置中的本地上传图片，不再提供独立图片上传入口。

## 当前目标

- 用户输入视频主题，内部写入 `theme_text`。
- 用户点击 `生成视频标题/视频文案`。
- WebUI 本地同时生成 3 个标题候选和视频文案。
- 用户选择其中 1 个标题。
- 用户在 `视频设置` 中上传 1 张或多张餐厅图片。
- 用户选择封面图片，或选择自动。
- WebUI 调用 `restaurant_engine` 本地 pipeline。
- 输出并预览 `cover_image.png`。
- 展示 `cover_plan` / `cover_render_report` / `pipeline_report` 的必要摘要。

## 复用模块

WebUI 不重新实现封面生成逻辑，当前复用：

- `restaurant_engine.cover_planner.build_title_candidates`
- `restaurant_engine.storyboard_planner.build_mock_storyboard`
- `restaurant_engine.pipeline.run_pipeline`
- `restaurant_engine.cover_planner`
- `restaurant_engine.cover_renderer`

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
- 不再简单拼接 `主题 + 后缀`。
- 当前按本地规则生成更适合短视频封面主标题的 3 个角度：
  - 味道钩子
  - 场景钩子
  - 氛围/发现感钩子
- 仍为 deterministic 本地模板，不调用 DeepSeek、LLM 或外部 API。

视频文案当前复用 `restaurant_engine` mock storyboard 能力生成，仅作为 WebUI 临时验证入口的本地文案展示，不调用 DeepSeek、LLM 或外部 API。

## 临时目录

上传图片和 pipeline 输出写入仓库外临时目录：

```text
/private/tmp/mpt-restaurant-webui/
```

每次生成封面会创建独立 run 目录，包含：

- `project.json`
- `images/`
- `output/cover_plan.json`
- `output/cover_render_report.json`
- `output/cover_image.png`
- `output/pipeline_report.json`

这些文件不得提交 Git。

## project.json 字段

WebUI 临时入口会生成 `pipeline_mode=cover_prototype` 的临时 project：

```json
{
  "pipeline_mode": "cover_prototype",
  "theme_text": "...",
  "selected_cover_title_id": "title_2",
  "selected_cover_image_id": "image_001",
  "image_dir": "images",
  "target_duration_seconds": 30
}
```

`pipeline_mode=cover_prototype` 只用于 WebUI 封面验证入口，允许封面验证在上传 1 张图片时运行，不改变默认视频主流程的图片数量和类别门禁。

## UI 行为

- 主按钮位于现有左侧 `文案设置` 区域，显示为 `生成视频标题/视频文案`。
- 点击主按钮后，按钮下方显示 3 个标题候选，视频文案写入现有 `视频文案` 输入框。
- 在餐饮封面 prototype 流程中，该按钮走本地安全路径：
  - 调用 `restaurant_engine.cover_planner.build_title_candidates` 生成 3 个 `local_static` 标题候选。
  - 复用本地 mock storyboard 能力生成 prototype 视频文案。
  - 不进入原 LLM 文案生成路径。
  - 不调用 DeepSeek、外部 API 或任何 LLM。
- prototype 视频文案只用于第 4 阶段 WebUI 临时验证入口，不是第 5 阶段正式文案系统。
- 不再要求用户单独点击 `生成标题候选`。
- 封面验证入口位于中间列 `视频设置` 区域的 `当前本地图片数量` 下方，按钮显示为 `生成封面`。
- 封面验证区不再显示独立主题输入、独立标题/文案生成按钮或独立图片上传入口。
- 未生成并选择标题时点击生成封面，WebUI 显示受控提示，不调用 pipeline。
- 用户选择具体上传图片时，WebUI 写入 `selected_cover_image_id`。
- 用户选择“自动选择”时，不写入 `selected_cover_image_id`，由 `cover_plan` 根据本地规则选择。
- 未上传图片时点击生成封面，WebUI 显示受控提示，不调用 pipeline。
- 成功后展示 `cover_image.png` 和封面摘要。

## 安全边界

当前入口：

- 不调用 DeepSeek。
- 不调用任何外部 API。
- 不调用 LLM。
- 不读取 API Key。
- 不调用视觉模型。
- 不使用 AI 图片生成。
- 不调用 TTS。
- 不生成音频。
- 不生成视频。
- 不修改 MoneyPrinterTurbo 原有视频生成主链路。
- 不写入 `storage/`。
- 不写入 `resource/`。
- 不写入仓库源码目录的 output。

## 当前边界

- 这是临时 prototype / validation 入口。
- 不是最终产品 UI。
- 不进入第 5 阶段。
- 图片理解默认使用 `mock` provider，不读取图片语义。
- 封面渲染使用本地 `local_pillow` renderer。
