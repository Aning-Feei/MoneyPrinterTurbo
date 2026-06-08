# 餐厅视频预检器说明

## 目的

第 2 阶段预检器用于在生成视频前，对餐厅视频项目做纯本地规则检查，并给出 WebUI 参数建议。

预检器只做：
- 镜头顺序计划
- 旁白时长估算
- `video_clip_duration` 建议
- 图片循环风险判断
- WebUI 参数建议
- warnings/errors 输出

预检器不会：
- 调用外部 API
- 调用 DeepSeek
- 调用 TTS
- 读取图片内容做视觉识别
- 生成视频
- 修改 MoneyPrinterTurbo 原有业务代码

## 输入

命令行接收仓库外样本项目的 `project.json`：

```bash
python -m restaurant_engine.preflight_project /Users/feei/AI/restaurant-video-ai-samples/sichuan_001/project.json
```

预检器复用现有 `project.json` 字段，并从以下字段读取旁白文本：

- `narration`
- `voiceover`
- `script`
- `text`
- `description`
- `video_script`
- `user_request`

如果没有专门旁白字段，当前会使用 `user_request` 作为时长估算兜底，并输出 warning。

新样本应显式填写：

```json
{
  "target_duration_seconds": 40
}
```

合法值为 `30`、`40`、`50`、`60`。旧样本如果缺少该字段，当前阶段可兼容，但应提示 warning。

## 输出

预检报告写入 `project.json` 同目录：

```text
preflight_report.json
```

核心输出结构：

- `ok`
- `project_id`
- `shot_plan`
- `timing`
- `render_params`
- `issues`

`timing` 当前包含：

- `target_duration_seconds`
- `estimated_narration_seconds`
- `recommended_clip_duration`
- `total_image_duration`
- `narration_safe_seconds`
- `narration_max_cjk_chars`
- `will_loop`

## CLI 退出码

- `0`：预检通过，报告 `ok` 为 `true`。
- `1`：预检已完成并写出报告，但存在 validation errors，报告 `ok` 为 `false`。这不是 Python 程序崩溃。
- 程序异常：例如无法写入报告等执行失败，会打印具体错误原因，例如 `preflight failed: ...`。

当退出码为 `1` 时，CLI 会明确打印：

```text
preflight completed with validation errors: 预检已完成，但存在校验错误
```

## 镜头顺序规则

当前按文件名识别角色，并推荐稳定顺序：

1. `intro`
2. `interior`
3. `dish_1`
4. `dish_2`
5. `dining`
6. `extra`

更多图片保留稳定排序，不使用 random。

## 旁白时长估算规则

预检器不调用 TTS，只做粗略估算：

- 中文字符按每秒约 4.5 个字估算
- 英文单词按每分钟 150 词估算
- 最小返回 1 秒

估算结果只用于生成前参数建议，不代表真实 TTS 音频时长。

## 目标时长和动态 clip duration 规则

预检器以 `target_duration_seconds` 作为主要时长目标，并根据图片数量动态推荐每张图片展示时长：

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
- 如果 WebUI 中实际使用的 `video_script` 比 preflight 输入文案更长，需要重新跑 preflight。

## 图片数量范围

按 3-6 秒/张反推，餐厅项目第一版建议：

| 目标时长 | 合理图片数量范围 |
|---|---:|
| 30 秒 | 6-10 张 |
| 40 秒 | 7-12 张 |
| 50 秒 | 9-16 张 |
| 60 秒 | 10-20 张 |

如果继续保留当前最大 12 张限制，50 秒和 60 秒仍可生成，但需要更谨慎控制文案和节奏。

图片太少应作为 error：

```text
image_count < ceil(target_duration_seconds / 6)
```

图片太多应作为 warning：

```text
image_count > floor(target_duration_seconds / 3)
```

## 旁白字数安全上限

为了减少真实 TTS 音频长于图片总时长导致循环的风险，预检报告应给出旁白最大中文字符数：

```text
narration_safe_seconds = target_duration_seconds - 3
narration_max_cjk_chars = floor(narration_safe_seconds * 4.0)
```

建议上限：

| 目标时长 | 旁白安全秒数 | 最大中文字符数 |
|---|---:|---:|
| 30 秒 | 27 秒 | 约 108 字 |
| 40 秒 | 37 秒 | 约 148 字 |
| 50 秒 | 47 秒 | 约 188 字 |
| 60 秒 | 57 秒 | 约 228 字 |

WebUI 实际 `video_script` 不应明显超过该字符上限。preflight/checklist 只能约束输入文案，无法保证用户在 WebUI 中手动粘贴的新文案仍符合约束。

如果当前输入旁白的中文字符数超过上限，预检器输出 warning：

- `narration_too_long_for_target_duration`

## WebUI 推荐参数

当前推荐：

- `video_source = local`
- `video_concat_mode = sequential`
- `video_clip_duration = recommended_clip_duration`

不要使用 random 作为餐厅镜头顺序基线。

## 循环风险规则

如果：

```text
图片数 * video_clip_duration < 估算旁白秒数
```

则认为存在图片循环风险，并输出 warning。建议增加图片、提高每张图片时长，或缩短旁白。

引入目标时长后，循环风险应同时考虑目标时长和估算旁白时长：

```text
total_image_duration < max(target_duration_seconds, estimated_narration_seconds)
```

如果图片覆盖时长短于目标时长，输出 warning：

- `image_duration_shorter_than_target_duration`

如果图片覆盖时长短于估算旁白时长，输出 warning：

- `image_duration_shorter_than_narration`

## 负向测试记录

已使用临时目录完成一次负向测试：

- 临时目录：/tmp/mpt-preflight-negative/
- 临时 project：/tmp/mpt-preflight-negative/project.json
- 临时报告：/tmp/mpt-preflight-negative/preflight_report.json
- 仓库内未出现 preflight_report.json
- 输入：
  - 3 张图片：01_intro.jpg、02_interior.jpg、03_dish_1.jpg
  - 较长旁白
- 输出摘要：
  - ok: false
  - estimated_narration_seconds: 31.78
  - recommended_clip_duration: 8
  - will_loop: true
  - video_source: local
  - video_concat_mode: sequential
  - video_clip_duration: 8
- 识别到的问题：
  - too_few_images：只有 3 张图，少于最低 6 张
  - missing_image_category：缺少 dish_2
  - missing_image_category：缺少 dining/gathering
  - missing_image_category：缺少 extra
  - image_duration_shorter_than_narration：3 张 * 8 秒 = 24 秒，小于估算旁白 31.78 秒，可能循环图片

结论：预检器能把 `video_clip_duration` 提高到上限 8 秒；当仍不足覆盖旁白时，会输出 `will_loop: true` 和 warning。命令退出码为 1 是因为报告 `ok: false`，属于负向测试预期，不是程序崩溃。

已改进 CLI 输出：当预检完成但 `ok=false` 时，会明确打印 `preflight completed with validation errors: 预检已完成，但存在校验错误`，避免误判为程序崩溃。

## 当前限制

- 不读取图片内容，不做视觉识别。
- 不生成真实分镜文案。
- 不保证估算时长与真实 TTS 完全一致。
- 不直接调用 MoneyPrinterTurbo WebUI 或业务代码。
