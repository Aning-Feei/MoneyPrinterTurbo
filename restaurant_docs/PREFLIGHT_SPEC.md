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

后续可改进 CLI 输出，让它更明确地区分“程序执行失败”和“预检完成但 ok=false”，例如输出 `preflight completed with validation errors`。

## 当前限制

- 不读取图片内容，不做视觉识别。
- 不生成真实分镜文案。
- 不保证估算时长与真实 TTS 完全一致。
- 不直接调用 MoneyPrinterTurbo WebUI 或业务代码。
