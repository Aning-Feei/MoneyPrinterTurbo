# 样本项目输入规范

## 样本项目目录结构

样本项目放在 MoneyPrinterTurbo 仓库外，避免把真实图片素材提交到 git。

```text
/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/
├── project.json
└── images/
    ├── 01_intro.jpg
    ├── 02_interior.jpg
    ├── 03_dish_1.jpg
    ├── 04_dish_2.jpg
    ├── 05_dining.jpeg
    └── 06_extra.jpg
```

## project.json 字段说明

- `project_name`：项目标识，用于生成输出目录和日志标识。
- `user_request`：用户对视频的自然语言需求描述。
- `selected_title`：封面和视频主标题。封面第一版只展示该主标题。
- `aspect_ratio`：视频比例，第一版默认使用 `9:16`。
- `voice_type`：口播音色或风格，例如 `female_energetic`。
- `voice_enabled`：是否生成 AI 旁白式口播。
- `subtitle_enabled`：是否生成字幕。
- `bgm_type`：BGM 风格，例如 `lively`。
- `video_style`：视频整体风格，例如 `烟火气`。
- `image_dir`：图片目录相对 project.json 所在目录的路径，第一版使用 `images`。
- `target_duration_seconds`：目标视频时长。新样本必须显式填写，合法值为 `30`、`40`、`50`、`60`。

示例：

```json
{
  "target_duration_seconds": 40
}
```

兼容策略：

- 旧样本如果缺少 `target_duration_seconds`，当前阶段可兼容，但应提示 warning。
- 新样本必须显式填写该字段，避免 WebUI 实际文案变长后图片总时长不足。

## 图片命名规则

- 文件格式支持 `.jpg`、`.jpeg`、`.png`。
- 建议使用有序前缀，便于控制视频顺序，例如 `01_intro.jpg`。
- 文件名应包含用途提示，便于第一版 pipeline 做规则判断。
- 不要把样本图片复制进 MoneyPrinterTurbo 仓库。

## 图片数量和目标时长规则

- 餐厅项目仍至少需要 6 张图片，以覆盖基础镜头类别。
- 后续第一版建议根据 `target_duration_seconds` 动态判断合理图片数量，而不是固定最多 12 张。
- 按 3-6 秒/张反推，建议范围：
  - 30 秒：6-10 张
  - 40 秒：7-12 张
  - 50 秒：9-16 张
  - 60 秒：10-20 张
- 如果继续保留当前最大 12 张限制，50 秒和 60 秒仍可生成，但需要更谨慎控制文案和节奏。

图片太少应作为 error：

```text
image_count < ceil(target_duration_seconds / 6)
```

图片太多应作为 warning：

```text
image_count > floor(target_duration_seconds / 3)
```

## 最低图片类别要求

- `intro`、`storefront` 或 `dish`：门头或招牌菜引入图，至少 1 张。
- `interior`：店内环境图，至少 1 张。
- `dish_1`：招牌菜 1，至少 1 张。
- `dish_2`：招牌菜 2，至少 1 张。
- `dining` 或 `gathering`：顾客就餐或聚餐氛围图，至少 1 张。
- `extra`：补充图，至少 1 张。

## 动态 video_clip_duration 规则

后续预检器应根据目标时长和图片数量推荐每张图片展示时长：

```text
raw_clip_duration = ceil(target_duration_seconds / image_count)
recommended_clip_duration = clamp(raw_clip_duration, 3, 6)
total_image_duration = image_count * recommended_clip_duration
will_loop = total_image_duration < max(target_duration_seconds, estimated_narration_seconds)
```

说明：

- 推荐每张图 3-6 秒。
- 低于 3 秒，画面切太快。
- 高于 6 秒，单图停留太久。
- 不建议依赖 random 或自动循环补齐素材。

## 旁白字数安全上限

为了减少 WebUI 实际文案变长导致图片重复播放的风险，新样本应按目标时长控制旁白长度：

```text
narration_safe_seconds = target_duration_seconds - 3
narration_max_cjk_chars = floor(narration_safe_seconds * 4.0)
```

建议上限：

- 30 秒：旁白安全秒数 27 秒，最大约 108 中文字符
- 40 秒：旁白安全秒数 37 秒，最大约 148 中文字符
- 50 秒：旁白安全秒数 47 秒，最大约 188 中文字符
- 60 秒：旁白安全秒数 57 秒，最大约 228 中文字符

WebUI 实际 `video_script` 不应明显超过该字符上限。如果在 WebUI 中改写文案或 AI 生成了更长文案，必须重新跑 preflight。preflight/checklist 只能约束输入文案，无法保证用户在 WebUI 中手动粘贴的新文案仍符合约束。

## 禁止上传内容

样本图片和后续用户上传图片中，不应包含：
- 电话
- 地址
- 二维码
- 菜单价格图

## 后续输入约定

后续 `restaurant_engine` pipeline 将以这个 `project.json` 作为输入，读取 `image_dir` 指向的图片目录，并输出：
- `image_understanding.json`
- `cover.jpg`
- `storyboard.json`
- `clips/`
- `final/final_video.mp4`
