# Image Understanding Contract 说明

本文件记录第 3 阶段 `restaurant_engine` 的图片理解 contract。

重要修正：正式产品不能依赖文件名识别图片类别。用户通常会从手机上传 `IMG_xxx`、微信图片等无语义文件名，因此图片理解主逻辑必须基于图片内容。当前代码只建立 provider 架构和 contract，不调用真实视觉模型或外部 API。

## 输出文件

示例路径：

```text
/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/output/image_understanding.json
```

顶层字段：

- `project_id`
- `version`
- `provider`
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
- `source`
- `detected_type`
- `quality_score`
- `cover_score`
- `video_score`
- `risk_score`
- `allowed_in_video`
- `recommended_usage`
- `recommended_action`
- `reason`

## Provider 模式

当前支持三个 provider：

- `mock`：默认 provider。只生成开发占位，不读取图片内容，也不使用文件名语义判断类别。
- `filename_fallback`：文件名兜底 provider。仅用于开发测试或没有视觉模型时的 fallback，不作为正式产品判断依据。
- `vision`：未来真实视觉 provider。必须显式指定并授权外部 API，当前尚未实现。

默认行为：

```bash
python3 -m restaurant_engine.pipeline_project \
  --project /path/to/project.json
```

等价于：

```bash
python3 -m restaurant_engine.pipeline_project \
  --project /path/to/project.json \
  --image-understanding-provider mock
```

未来真实视觉识别必须显式开启：

```bash
python3 -m restaurant_engine.pipeline_project \
  --project /path/to/project.json \
  --image-understanding-provider vision \
  --allow-external-api
```

当前 `vision` provider 仍是占位，未接真实视觉模型，不会调用外部 API。

## 正式视觉识别目标

未来 `vision` provider 应基于图片内容识别：

- 门头 / 招牌 / 店铺外观
- 店内环境
- 菜品
- 后厨 / 制作过程
- 顾客用餐
- 聚餐氛围
- 菜单 / 价格 / 二维码 / 电话 / 地址 / 联系方式等禁用内容
- 模糊 / 低质量 / 纯文字海报

## Mock Provider

`mock` provider 用于本地开发和 contract 联调：

- 不读取图片像素。
- 不解析文件名语义。
- 不调用视觉模型。
- 不调用 OCR。
- 不调用外部 API。
- 每张图输出 `detected_type=unknown`、`source=mock`、`recommended_action=review`。

## Filename Fallback Provider

`filename_fallback` 只作为兜底，不是正式图片理解能力。

文件名拒绝规则：

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

## Mock / Fallback 分数

当前分数只用于 contract 占位，不代表真实图片质量。

| detected_type | quality_score | cover_score | video_score | risk_score |
|---|---:|---:|---:|---:|
| unknown | 0.50 | 0.50 | 0.50 | 0.10 |
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
- 默认 provider 为 `mock`，不调用视觉模型、OCR、DeepSeek、TTS 或任何外部 API。
- `filename_fallback` 必须显式指定，只能作为开发 fallback。
- `vision` 必须显式指定并传入 `--allow-external-api`，当前尚未实现。
- 本阶段不生成音频、不生成视频。

## 后续增强

- 替换文件名规则为真实视觉理解模型。
- 引入 OCR，识别二维码、电话、地址、菜单价格等风险内容。
- 引入图片清晰度、主体占比、重复度、横竖构图检测。
- 根据 `cover_score` 自动推荐封面。
- 根据 `video_score` 和 `risk_score` 决定图生视频输入清单。
