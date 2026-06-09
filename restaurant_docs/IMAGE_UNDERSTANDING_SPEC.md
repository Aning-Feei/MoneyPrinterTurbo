# Mock Image Understanding 说明

本文件记录第 2 阶段 `restaurant_engine` 的 mock 图片理解 contract。

当前目标是在接入真实视觉模型、OCR、封面筛选和图生视频前，先生成一个稳定的本地 `image_understanding.json`。本阶段只使用文件名规则，不读取图片内容，不调用外部 API。

## 输出文件

示例路径：

```text
/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/output/image_understanding.json
```

顶层字段：

- `project_id`
- `version`
- `image_dir`
- `image_count`
- `allowed_image_count`
- `rejected_image_count`
- `images`
- `category_counts`
- `warnings`
- `errors`
- `notes`

单张图片字段：

- `image_id`
- `filename`
- `image_path`
- `detected_type`
- `quality_score`
- `cover_score`
- `video_score`
- `risk_score`
- `allowed_in_video`
- `recommended_usage`
- `recommended_action`
- `reason`

## 文件名规则

拒绝进入视频：

- `qrcode` / `qr` -> `invalid_qrcode`
- `phone` / `tel` -> `invalid_phone`
- `address` -> `invalid_address`
- `menu` -> `invalid_menu`
- `price` -> `invalid_price`
- `contact` -> `invalid_contact`
- `wechat` / `wx` -> `invalid_wechat`

可用类型：

- `intro` / `storefront` / `front` / `sign` / `door` -> `intro`
- `interior` / `inside` / `room` / `hall` / `environment` -> `interior`
- `dish_1` / `dish1` / `dish_2` / `dish_3` / `dish` / `food` / `cuisine` / `meal` -> `dish`
- `dining` / `gathering` / `table` / `friends` / `family` -> `dining`
- `detail` / `sauce` / `soup` / `pot` / `ingredient` -> `detail`
- `extra` -> `extra`
- `logo` -> `logo`
- 其他 -> `other`

## Mock 分数

当前分数只用于 contract 占位，不代表真实图片质量。

| detected_type | quality_score | cover_score | video_score | risk_score |
|---|---:|---:|---:|---:|
| intro | 0.75 | 0.85 | 0.75 | 0.05 |
| interior | 0.75 | 0.55 | 0.80 | 0.05 |
| dish | 0.80 | 0.90 | 0.85 | 0.05 |
| dining | 0.75 | 0.65 | 0.85 | 0.05 |
| detail | 0.65 | 0.55 | 0.65 | 0.10 |
| extra | 0.65 | 0.55 | 0.65 | 0.10 |
| other | 0.65 | 0.55 | 0.65 | 0.10 |
| invalid_* | 0.20 | 0.00 | 0.00 | 0.95 |

## 推荐动作

- `intro` / `dish`：`recommended_usage=cover_candidate`
- `interior` / `dining`：`recommended_usage=video_scene`
- `detail` / `extra`：`recommended_usage=support`
- `other` / `logo`：`recommended_action=review`
- `invalid_*`：`allowed_in_video=false`，`recommended_action=reject`

## Pipeline 边界

- `build_image_understanding` 在图片扫描后、storyboard planning 前执行。
- `write_image_understanding` 输出 `image_understanding.json`。
- 拒绝图片当前只产生 warning，不阻断 pipeline。
- 没有图片时产生 error，pipeline `ok=false`。
- 本阶段不调用视觉模型、OCR、DeepSeek、TTS 或任何外部 API。
- 本阶段不生成音频、不生成视频。

## 后续增强

- 替换文件名规则为真实视觉理解模型。
- 引入 OCR，识别二维码、电话、地址、菜单价格等风险内容。
- 引入图片清晰度、主体占比、重复度、横竖构图检测。
- 根据 `cover_score` 自动推荐封面。
- 根据 `video_score` 和 `risk_score` 决定图生视频输入清单。
