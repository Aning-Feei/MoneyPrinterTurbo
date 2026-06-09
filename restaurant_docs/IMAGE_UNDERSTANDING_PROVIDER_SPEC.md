# Image Understanding Provider 架构说明

本文件记录第 3 阶段图片理解 provider 架构调整。

## 背景修正

原先第 2 阶段为了补齐 `image_understanding.json`，实现了基于文件名规则的 mock 图片理解。用户确认真实产品中图片来自手机上传，文件名通常没有语义，不能作为门头、菜品、店内环境、聚餐等类别判断依据。

因此第 3 阶段调整为：

- 图片内容识别是正式主逻辑。
- 文件名规则只能作为开发 fallback。
- 默认仍不调用外部 API。
- 真实视觉识别未来必须显式开启。

## Provider 列表

| Provider | 默认 | 是否看图片内容 | 是否使用文件名语义 | 是否调用外部 API | 用途 |
|---|---|---|---|---|---|
| `mock` | 是 | 否 | 否 | 否 | 本地开发占位与 contract 联调 |
| `filename_fallback` | 否 | 否 | 是 | 否 | 没有视觉模型时的开发兜底 |
| `vision` | 否 | 是 | 否 | 未来需要 | 正式图片理解主逻辑 |

## CLI 约束

默认命令不调用外部 API：

```bash
python3 -m restaurant_engine.pipeline_project \
  --project /path/to/project.json
```

显式文件名 fallback：

```bash
python3 -m restaurant_engine.pipeline_project \
  --project /path/to/project.json \
  --image-understanding-provider filename_fallback
```

未来真实视觉 provider 必须显式开启：

```bash
python3 -m restaurant_engine.pipeline_project \
  --project /path/to/project.json \
  --image-understanding-provider vision \
  --allow-external-api
```

当前 `vision` provider 尚未接入真实模型。即使传入 `--allow-external-api`，也会返回未实现错误，不会调用外部 API。

## 输出 Contract

`image_understanding.json` 顶层必须记录：

- `provider`
- `version`
- `image_count`
- `allowed_image_count`
- `rejected_image_count`
- `category_counts`
- `warnings`
- `errors`

每张图片必须记录：

- `source`
- `detected_type`
- `allowed_in_video`
- `recommended_usage`
- `recommended_action`
- `reason`

`source` 用于区分判断来源：

- `mock`
- `filename_fallback`
- 未来 `vision`

## 正式 Vision Provider 目标

未来 `vision` provider 应基于图片内容完成：

- 餐厅类别识别：门头、店内、菜品、后厨、顾客用餐、聚餐氛围。
- 风险识别：二维码、电话、地址、联系方式、菜单价格、纯文字海报。
- 质量识别：模糊、过暗、低分辨率、重复度、主体不清。
- 使用建议：是否适合封面、是否适合进入视频、是否需要人工复核。

## 当前边界

- 不调用 DeepSeek。
- 不调用任何外部 API。
- 不调用 TTS。
- 不调用视觉模型或 OCR。
- 不生成音频。
- 不生成视频。
- 不修改 WebUI、`app/`、`config.toml` 或 MoneyPrinterTurbo 视频生成核心。
