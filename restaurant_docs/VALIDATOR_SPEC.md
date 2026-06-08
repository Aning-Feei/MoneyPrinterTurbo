# restaurant_engine 只读校验器说明

## 用途

`restaurant_engine` 当前阶段只做项目输入校验，用于确认仓库外样本项目是否满足餐饮 AI 宣传视频生成系统的最低输入要求。

校验器不会：
- 生成视频
- 调用 DeepSeek
- 调用 TTS
- 调用 AI 图生视频服务
- 读取图片内容或做视觉识别
- 修改 MoneyPrinterTurbo 原有业务代码
- 复制样本图片进 MoneyPrinterTurbo 仓库

## 输入 project.json

命令行入口接收仓库外样本项目的 `project.json`：

```text
/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/project.json
```

必填字段：
- `project_name`
- `user_request`
- `selected_title`
- `aspect_ratio`
- `voice_type`
- `voice_enabled`
- `subtitle_enabled`
- `bgm_type`
- `video_style`
- `image_dir`

`aspect_ratio` 只能是：
- `9:16`
- `16:9`

`image_dir` 是相对 `project.json` 所在目录的图片目录路径。

## 图片数量规则

- 至少 6 张图片
- 最多 12 张图片
- 支持 `.jpg`、`.jpeg`、`.png`

## 命名类别规则

图片文件名需要覆盖以下类别：
- `intro`、`storefront` 或 `dish`：引入图至少 1 张
- `interior`：店内环境图至少 1 张
- `dish_1`：招牌菜 1 至少 1 张
- `dish_2`：招牌菜 2 至少 1 张
- `dining` 或 `gathering`：顾客就餐或聚餐氛围图至少 1 张
- `extra`：补充图至少 1 张

## 禁止内容占位规则

当前阶段不读取图片内容，只通过文件名做风险占位检查。

如果图片文件名包含以下关键词，会标记为禁止内容风险：
- `qrcode`
- `qr`
- `phone`
- `tel`
- `address`
- `menu`
- `price`
- `contact`
- `wechat`
- `wx`

后续视觉识别阶段再补充真实图片内容检查。

## 命令行用法

在 MoneyPrinterTurbo 项目根目录执行：

```bash
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
uv run python -m restaurant_engine.validate_project --project /Users/feei/AI/restaurant-video-ai-samples/sichuan_001/project.json
```

## 输出 validation_report.json 示例结构

校验报告写到样本项目目录，不写入 MoneyPrinterTurbo 仓库：

```text
/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/validation_report.json
```

示例结构：

```json
{
  "project_path": "/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/project.json",
  "project_name": "sichuan_001",
  "image_dir": "/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/images",
  "image_count": 6,
  "image_files": [
    "01_intro.jpg",
    "02_interior.jpg",
    "03_dish_1.jpg",
    "04_dish_2.jpg",
    "05_dining.jpeg",
    "06_extra.jpg"
  ],
  "category_checks": {
    "intro_or_storefront_or_dish": true,
    "interior": true,
    "dish_1": true,
    "dish_2": true,
    "dining_or_gathering": true,
    "extra": true
  },
  "issues": [],
  "passed": true
}
```
