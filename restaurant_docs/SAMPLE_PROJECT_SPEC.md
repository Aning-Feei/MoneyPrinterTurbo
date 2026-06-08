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

## 图片命名规则

- 文件格式支持 `.jpg`、`.jpeg`、`.png`。
- 建议使用有序前缀，便于控制视频顺序，例如 `01_intro.jpg`。
- 文件名应包含用途提示，便于第一版 pipeline 做规则判断。
- 不要把样本图片复制进 MoneyPrinterTurbo 仓库。

## 最低图片类别要求

- 至少 6 张，最多 12 张。
- `intro`、`storefront` 或 `dish`：门头或招牌菜引入图，至少 1 张。
- `interior`：店内环境图，至少 1 张。
- `dish_1`：招牌菜 1，至少 1 张。
- `dish_2`：招牌菜 2，至少 1 张。
- `dining` 或 `gathering`：顾客就餐或聚餐氛围图，至少 1 张。
- `extra`：补充图，至少 1 张。

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
