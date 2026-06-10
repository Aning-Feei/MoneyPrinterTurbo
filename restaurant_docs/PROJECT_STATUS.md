# 项目状态

## 项目基本信息

- 项目名称：餐饮 AI 宣传视频生成系统
- 当前仓库：/Users/feei/AI/MoneyPrinterTurbo
- 当前分支：feature/restaurant-video-prototype
- 当前阶段：第 2 阶段：餐厅专用镜头计划 / 参数预检器（WebUI 餐厅视频模式实现中）
- 当前下一步：在 WebUI 中直接提供餐厅视频模式、目标时长选择、图片数量拦截和文案长度提示；第一版不改视频合成核心。

## 当前样本项目

- 当前样本项目路径：/Users/feei/AI/restaurant-video-ai-samples/sichuan_001
- 当前样本图片目录：/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/images
- 当前样本 project.json：/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/project.json

## 已完成事项

1. 修复 Codex service_tier 配置问题
2. 确认 Codex 正确进入 MoneyPrinterTurbo 目录
3. 创建 feature/restaurant-video-prototype 分支
4. 创建 restaurant_docs/
5. 创建 restaurant_engine/
6. 创建 restaurant_docs/README.md
7. 创建 restaurant_docs/PROJECT_PLAN.md
8. 创建 restaurant_docs/SAMPLE_PROJECT_SPEC.md
9. 准备仓库外样本图片目录
10. 样本图片已满足 6 张最低要求
11. 创建样本 project.json
12. 创建 restaurant_docs/CODEX_CONTROL_RULES.md
13. 创建 restaurant_engine 最小只读校验器
14. 完成 WebUI 启动和浏览器冒烟测试
15. 定位 WebUI 基础生成测试产物路径
16. 完成人工播放检查 final-1.mp4
17. 完成图片顺序不合理的只读根因定位
18. 完成第二次 WebUI Sequential 复测和循环原因定位
19. 完成第三次 WebUI 参数基线复测
20. 开始第 2 阶段并实现最小版预检器
21. 完成第 2 阶段预检器负向测试
22. 改进预检器 CLI ok=false 提示
23. 新增 WebUI 操作清单工具
24. 增强 WebUI 操作清单字段映射
25. 完成 hotpot_001 第二样本半自动流程验证并发现目标时长/文案长度问题

## 当前阻塞点

无

## 下一步目标

增加更清晰的 WebUI 参数填表指南，或把 preflight_report.json 转成“人工操作清单”；也可以继续做结构化镜头计划，但仍暂不改 MoneyPrinterTurbo 原业务代码。

## 第 0 阶段 0.9 状态

已完成。已创建只读校验器，读取仓库外 project.json，验证字段、图片数量、命名类别和禁止内容占位规则，只输出 validation_report.json，不生成视频。

## 第 1 阶段状态

已通过。本阶段已完成基础生成链路只读检查、WebUI 启动和浏览器冒烟测试，定位到最终视频候选文件，并完成人工播放检查。

## 第 1 阶段 WebUI 冒烟测试状态

- WebUI 启动命令：sh ./webui.sh
- WebUI 地址：http://127.0.0.1:8501
- WebUI 已启动成功，进程仍在运行
- 浏览器测试结果：
  - WebUI 打开成功
  - 页面无红色报错
  - 主要页面/Tab 可用
  - 已点击生成按钮
  - 用户反馈已调用外部 API
  - 用户反馈已生成文件
  - 终端暂无新增错误日志
- 生成文件路径：storage/tasks/6b4c0e38-8df8-4991-87cd-ad495ab090df/final-1.mp4
- 生成文件名：final-1.mp4
- 外部 API provider：待补充，用户未提供具体 provider
- 本轮未发现页面红色报错，终端暂无新增错误日志。

## 第 1 阶段生成产物定位

- task_id：6b4c0e38-8df8-4991-87cd-ad495ab090df
- 最终视频候选：
  - storage/tasks/6b4c0e38-8df8-4991-87cd-ad495ab090df/final-1.mp4，约 1.6M
- 合成中间视频：
  - storage/tasks/6b4c0e38-8df8-4991-87cd-ad495ab090df/combined-1.mp4，约 1.6M
- TTS 音频：
  - storage/tasks/6b4c0e38-8df8-4991-87cd-ad495ab090df/audio.mp3，约 29K
- 字幕文件：
  - storage/tasks/6b4c0e38-8df8-4991-87cd-ad495ab090df/subtitle.srt，约 128B
- 脚本/任务参数：
  - storage/tasks/6b4c0e38-8df8-4991-87cd-ad495ab090df/script.json，约 2.0K
- 本地图片预处理生成的中间视频：
  - storage/local_videos/54aa385e-f487-48a8-b763-69ac1ef95d30_01_intro.jpg.mp4，约 1.9M
  - storage/local_videos/1abcd369-c7d5-47e6-bc83-c56179d41f90_03_dish_1.jpg.mp4，约 1.5M
  - storage/local_videos/9f82f6d5-9225-4515-be68-45b888ba1d1b_04_dish_2.jpg.mp4，约 1.3M
- 日志状态：
  - 发现非生成链路错误：osascript 尝试访问 chrome/firefox/safari 的错误
  - 发现 st.components.v1.html deprecation 提示
  - 未发现 TTS、字幕、BGM、ffmpeg 失败日志
  - 日志明确显示任务成功：generated 1 videos
- 当前结论：
  - WebUI 页面打开成功
  - 点击生成后成功调用外部 API
  - 成功生成最终视频候选文件
  - 第 1 阶段基础生成链路冒烟测试通过
- 下一步建议：
  - 人工播放 final-1.mp4，检查画面、字幕、语音、时长、餐厅图片顺序
  - 决定是否将 storage/、生成视频、音频、字幕等加入 .gitignore
  - 暂不把生成产物提交到 Git

## 第 1 阶段人工播放检查

- 检查视频：
  - /Users/feei/AI/MoneyPrinterTurbo/storage/tasks/6b4c0e38-8df8-4991-87cd-ad495ab090df/final-1.mp4
- 用户人工检查结果：
  - 视频可以正常播放
  - 视频使用了餐厅图片
  - 图片顺序不合理
  - 语音正常
  - 字幕正常
  - 字幕和语音同步情况：待确认，用户未明确反馈
  - 视频节奏可接受
- 当前结论：
  - 第 1 阶段 WebUI 基础生成链路通过
  - 当前最大问题不是生成失败，而是素材顺序/镜头编排不符合预期
- 下一步建议：
  - 只读分析图片输入顺序、脚本片段顺序、local_videos 生成顺序、最终合成顺序之间的关系
  - 暂不修改业务代码

## 第 1 阶段图片顺序根因定位

- 目标 task：
  - 6b4c0e38-8df8-4991-87cd-ad495ab090df
- 最终视频：
  - storage/tasks/6b4c0e38-8df8-4991-87cd-ad495ab090df/final-1.mp4
- script.json 中 video_materials 顺序：
  1. 01_intro.jpg
  2. 03_dish_1.jpg
  3. 04_dish_2.jpg
- script.json 中 video_concat_mode：
  - random
- WebUI 日志中的预处理顺序：
  1. 01_intro
  2. 03_dish_1
  3. 04_dish_2
- 最终合成日志显示 combined-1.mp4 的处理顺序开头：
  1. 03_dish_1
  2. 01_intro
- 04_dish_2 未进入最终合成的可能原因：
  - 旁白音频约 4.87 秒
  - 每段图片视频约 3 秒
  - 最终只覆盖约 2 个 clip
- 代码只读定位：
  - app/services/video.py 中 _prioritize_unique_source_clips(...) 在 VideoConcatMode.random 下会 random.shuffle(primary_items)
- 当前最可能原因：
  - 最终合成阶段的 random 模式打乱了素材顺序
- 次要原因：
  - 本次只实际使用了 3 张图片，不是完整 6 张样本
  - 旁白过短，无法覆盖所有图片
  - script.json 没有 scene-to-image mapping
- 当前决定：
  - 暂不实施代码修改
- 下一步建议：
  - 无代码复测：上传完整 6 张样本图片
  - WebUI 拼接模式选择 Sequential/顺序拼接，不使用 random
  - 使用更长旁白，至少覆盖 6 张图 * 3 秒，约 18 秒以上
  - 如果无代码复测通过，再决定是否需要代码层强制顺序模式
  - 如果后续做餐厅专用引擎，应在 restaurant_engine 层生成明确镜头顺序计划，不依赖 WebUI random 合成

## 第 1 阶段第二次 Sequential 复测

- task_id：
  - 57ddf7ec-e50b-4b03-be4f-714deabdeafc
- 复测设置：
  - 上传完整 6 张图片：是
  - 拼接模式：Sequential/顺序
  - 使用更长旁白：是
  - video_clip_duration：3 秒
- 复测结果：
  - 生成 final-1.mp4：是
  - 视频正常播放：是
  - 图片顺序正确：是
  - 6 张图片都出现：是
  - 语音正常：是
  - 字幕正常：是
  - 字幕和语音同步：是
  - 节奏可接受：是
  - 终端无新错误
  - 最大问题：视频播放了两遍图片
- 产物信息：
  - storage/tasks/57ddf7ec-e50b-4b03-be4f-714deabdeafc/final-1.mp4，约 9.6M，时长 00:00:33.00，分辨率 1080x1920
  - storage/tasks/57ddf7ec-e50b-4b03-be4f-714deabdeafc/audio.mp3，约 181K，时长 00:00:30.91
  - storage/tasks/57ddf7ec-e50b-4b03-be4f-714deabdeafc/script.json，约 3.5K
  - storage/tasks/57ddf7ec-e50b-4b03-be4f-714deabdeafc/subtitle.srt，约 807B
  - storage/tasks/57ddf7ec-e50b-4b03-be4f-714deabdeafc/combined-1.mp4，约 9.1M
- script.json 关键信息：
  - video_concat_mode 为 sequential
  - video_materials 数量为 6，顺序完整且正确：
    1. 01_intro.jpg
    2. 02_interior.jpg
    3. 03_dish_1.jpg
    4. 04_dish_2.jpg
    5. 05_dining.jpeg
    6. 06_extra.jpg
  - 没有发现 clips/scenes/duration 的结构化镜头字段
  - video_clip_duration 为 3
- 只读日志定位结论：
  - 音频时长：30.91 秒
  - 每段图片视频最大时长：3 秒
  - 原始 6 个 clip 总时长约：18.00 秒
  - 日志显示：video duration (18.00s) is shorter than audio duration (30.91s), looping clips to match audio length.
  - 日志显示：looped 5 clips
  - 日志显示：concatenating 11 clips with ffmpeg
- 当前结论：
  - 第一次图片顺序问题已通过 WebUI 选择 Sequential/顺序拼接解决
  - 第二次复测证明：顺序模式有效，完整 6 张图能按正确顺序进入最终视频
  - 当前新问题不是顺序错误，而是画面总时长不足导致系统循环图片
  - 重复播放根因：6 张图 * 3 秒 = 18 秒，短于 30.91 秒旁白，所以 Sequential 模式下仍会循环已有 clip 补足音频
- 下一步建议：
  - 第三次无代码复测：继续使用完整 6 张图片
  - 继续使用 Sequential/顺序拼接
  - 保持当前长旁白
  - 将 video_clip_duration 从 3 秒提高到 6 秒
  - 目标：6 张图 * 6 秒 = 36 秒，覆盖约 30.91 秒音频，验证是否不再循环图片
  - 暂不修改业务代码
  - 后续餐厅专用引擎应在生成前计算 图片数 * 每张时长 >= 旁白时长，并给出参数建议或自动调整

## 第 1 阶段第三次 WebUI 参数基线复测

- task_id：
  - 2dceacbf-bf55-494a-8004-a3f0eacfb067
- 复测设置：
  - 上传完整 6 张图片：是
  - 拼接模式：Sequential/顺序
  - 每张图片时长：6 秒
  - 使用同一段较长旁白：是
- 复测结果：
  - 生成 final-1.mp4：是
  - 视频正常播放：是
  - 图片顺序正确：是
  - 6 张图片都出现：是
  - 图片没有重复播放：是
  - 语音正常：是
  - 字幕正常：是
  - 字幕和语音同步：是
  - 节奏可接受：是
  - 终端无新错误
  - 当前最大问题：无
- 产物信息：
  - storage/tasks/2dceacbf-bf55-494a-8004-a3f0eacfb067/final-1.mp4，约 9.3M，时长 00:00:36.00，分辨率 1080x1920
  - storage/tasks/2dceacbf-bf55-494a-8004-a3f0eacfb067/audio.mp3，约 181K，时长 00:00:30.91
  - storage/tasks/2dceacbf-bf55-494a-8004-a3f0eacfb067/script.json，约 3.4K
  - storage/tasks/2dceacbf-bf55-494a-8004-a3f0eacfb067/subtitle.srt，约 807B
  - storage/tasks/2dceacbf-bf55-494a-8004-a3f0eacfb067/combined-1.mp4，约 8.7M
- script.json 关键信息：
  - video_concat_mode 为 sequential
  - video_clip_duration 为 6
  - video_materials 数量为 6，顺序完整且正确：
    1. 01_intro.jpg
    2. 02_interior.jpg
    3. 03_dish_1.jpg
    4. 04_dish_2.jpg
    5. 05_dining.jpeg
    6. 06_extra.jpg
- 日志定位结论：
  - 音频时长：30.91 秒
  - 每段图片视频最大时长：6 秒
  - 6 张图总可用时长约：36 秒
  - 未出现 looping clips to match audio length 提示
  - 日志显示：concatenating 6 clips with ffmpeg
- 当前结论：
  - 第三次 WebUI 复测通过
  - 第 1 阶段 WebUI 基础餐厅图文视频生成链路通过
  - 当前推荐 WebUI 参数基线：完整素材、Sequential/顺序拼接、video_clip_duration = 6，并确保 图片数 * 每张图片时长 >= 旁白时长
  - 暂不需要修改 MoneyPrinterTurbo 业务代码
- 下一阶段建议：
  - 固化餐厅样片输入规范
  - 整理 restaurant_engine 和文档结构
  - 规划餐厅专用镜头顺序/参数预检器
  - 决定如何处理 .gitignore 和未跟踪文档/代码

## 第 2 阶段状态

进行中。已实现最小版餐厅视频预检器：

- 输入：project.json + 图片目录 + 旁白文本
- 输出：preflight_report.json
- 能力：
  - 镜头顺序计划
  - 旁白时长估算
  - 推荐 video_clip_duration
  - 图片循环风险判断
  - WebUI 参数建议
  - warnings/errors
- 约束：
  - 纯本地规则
  - 不调用外部 API
  - 不调用 TTS
  - 不生成视频
  - 不修改 MoneyPrinterTurbo 原有业务代码

## 第 2 阶段负向测试

- 临时测试目录：/tmp/mpt-preflight-negative/
- 临时 project：/tmp/mpt-preflight-negative/project.json
- 临时报告：/tmp/mpt-preflight-negative/preflight_report.json
- 仓库内未出现 preflight_report.json
- 输入特征：
  - 只有 3 张图片：
    1. 01_intro.jpg
    2. 02_interior.jpg
    3. 03_dish_1.jpg
  - 旁白较长
- 运行结果：
  - 预检器运行成功
  - 命令退出码为 1
  - 退出码为 1 的原因是报告 ok: false，属于负向测试预期，不是程序崩溃
- 报告摘要：
  - ok: false
  - estimated_narration_seconds: 31.78
  - recommended_clip_duration: 8
  - will_loop: true
  - video_source: local
  - video_concat_mode: sequential
  - video_clip_duration: 8
- shots 顺序：
  1. intro / 01_intro.jpg / 8s
  2. interior / 02_interior.jpg / 8s
  3. dish_1 / 03_dish_1.jpg / 8s
- errors:
  - too_few_images：只有 3 张图，少于最低 6 张
  - missing_image_category：缺少 dish_2
  - missing_image_category：缺少 dining/gathering
  - missing_image_category：缺少 extra
- warning:
  - image_duration_shorter_than_narration：3 张 * 8 秒 = 24 秒，小于估算旁白 31.78 秒，可能循环图片
- 结论：
  - 预检器正确识别循环风险
  - 预检器会把 clip duration 提高到上限 8 秒
  - 当仍不足覆盖旁白时，会给出 will_loop: true 和 warning
  - 第 2 阶段最小版预检器通过负向测试
- 后续改进建议：
  - 已完成 CLI 提示改进：当预检完成但 ok=false 时，控制台会输出 preflight completed with validation errors: 预检已完成，但存在校验错误
  - 程序异常仍会打印 preflight failed: ... 形式的具体错误原因
  - 后续继续规划餐厅专用镜头顺序/参数预检规则

## 当前阶段收口总结

### 第 1 阶段完成状态

- WebUI 成功启动。
- WebUI 基础餐厅图文视频生成链路通过。
- 可用样片 task：
  - 2dceacbf-bf55-494a-8004-a3f0eacfb067
- 可用样片：
  - storage/tasks/2dceacbf-bf55-494a-8004-a3f0eacfb067/final-1.mp4
- 推荐 WebUI 参数基线：
  - 完整 6 张图
  - Sequential/顺序拼接
  - video_clip_duration = 6
  - 确保 图片数 * 每张图片时长 >= 旁白时长

### 第 2 阶段当前完成状态

- restaurant_engine 已有只读 validator。
- 已新增 preflight planner。
- 可生成 preflight_report.json。
- 已新增 WebUI 操作清单工具。
- 可把 preflight_report.json 转成 webui_checklist.md。
- 正向样本通过。
- 负向样本可识别：
  - 图片不足
  - 角色缺失
  - 循环风险
- CLI 已明确区分：
  - preflight completed successfully
  - preflight completed with validation errors: 预检已完成，但存在校验错误

### 当前代码边界

- 未修改 MoneyPrinterTurbo 原业务代码。
- 未接入 WebUI。
- 未调用外部 API。
- 不生成视频，只做生成前预检。
- 生成产物和 preflight_report.json 不进入 Git。

### 当前可用命令

- 校验器：
  - python3 -m restaurant_engine.validate_project /Users/feei/AI/restaurant-video-ai-samples/sichuan_001/project.json
- 预检器：
  - python3 -m restaurant_engine.preflight_project /Users/feei/AI/restaurant-video-ai-samples/sichuan_001/project.json
- WebUI 操作清单：
  - python3 -m restaurant_engine.webui_checklist /Users/feei/AI/restaurant-video-ai-samples/sichuan_001/preflight_report.json

### 下一步建议

- 增加更清晰的 WebUI 参数填表指南。
- 或把 preflight_report.json 转成“人工操作清单”。
- 或继续做结构化镜头计划，但仍暂不改 MoneyPrinterTurbo 原业务代码。
- 出差/换电脑前建议 push 当前分支到远程仓库。

## 餐厅视频半自动流程收口

当前半自动流程已形成：

```text
project.json
-> python3 -m restaurant_engine.validate_project <project.json>
-> python3 -m restaurant_engine.preflight_project <project.json>
-> python3 -m restaurant_engine.webui_checklist <preflight_report.json>
-> 人工按 webui_checklist.md 填 WebUI
-> 生成视频
```

### 当前已有工具

- restaurant_engine.validate_project
  - 只读校验 project.json 和图片素材规范
- restaurant_engine.preflight_project
  - 生成 preflight_report.json
  - 输出镜头顺序、旁白时长估算、clip duration 推荐、循环风险、WebUI 参数建议
- restaurant_engine.webui_checklist
  - 读取 preflight_report.json
  - 生成 webui_checklist.md
  - 正向样本提示可以生成
  - 负向样本提示不建议生成并列出风险
  - 写出真实 WebUI 字段名称、字段值和人工填表步骤

### 当前已验证

- 第 1 阶段：WebUI 餐厅图文视频样片跑通。
- 第 2 阶段：
  - preflight 正向样本通过
  - preflight 负向样本能发现图片不足、角色缺失、循环风险
  - checklist 正向样本能生成 WebUI 填表清单
  - checklist 负向样本能明确提示不建议生成

### 当前边界

- 未修改 MoneyPrinterTurbo 原业务代码。
- 未接入 WebUI 自动填表。
- 未调用外部 API。
- 未生成视频。
- 只做生成前校验、预检和人工操作清单。
- preflight_report.json 和 webui_checklist.md 生成在样本目录或临时目录，不进入 Git。
- storage/ 和生成产物不进入 Git。

### 当前建议下一步

- 可选方向 A：继续增强 webui_checklist.md，加入更具体的 WebUI 页面字段映射。
- 可选方向 B：增加结构化镜头计划字段，例如每个 shot 的标题、旁白片段、画面用途。
- 可选方向 C：准备 push 当前分支到 GitHub，方便换电脑继续。
- 不建议立即修改 MoneyPrinterTurbo 原业务代码。

## hotpot_001 第二样本问题记录

- 第二样本：
  - /Users/feei/AI/restaurant-video-ai-samples/hotpot_001/project.json
- 已完成验证：
  - validate_project 通过
  - preflight_project 通过
  - webui_checklist 生成成功
  - 用户按 checklist 在 WebUI 中生成视频
- checklist 推荐：
  - video_concat_mode = sequential
  - video_source = local
  - video_clip_duration = 5
- WebUI 实际结果：
  - final-1.mp4 已生成
  - 视频可正常播放
  - 使用了 hotpot_001 图片
  - 图片顺序正确
  - 6 张图片都出现
  - 语音、字幕正常且同步
  - 图片重复播放
- 只读定位结论：
  - WebUI 实际生成音频约 39.72 秒
  - 6 张图 * 5 秒 = 30 秒
  - 实际音频长于图片总时长，导致 Sequential 模式下仍需要重复图片补齐音频
- 当前结论：
  - 需要引入 `target_duration_seconds`
  - 需要根据目标时长和图片数量动态计算 `video_clip_duration`
  - 需要根据目标时长约束图片数量和旁白字数
  - preflight/checklist 只能约束输入文案，无法保证用户在 WebUI 中手动粘贴或 AI 改写的新文案仍符合约束
- 当前处理：
  - 先更新规格文档
  - 暂不修改 restaurant_engine 代码
  - 暂不修改 MoneyPrinterTurbo 原业务代码

## Step 2-1 validator 目标时长校验

- 当前目标：
  - 在 validator 层支持 `target_duration_seconds`
  - 合法值为 30、40、50、60
  - 旧样本缺少该字段时输出 warning，不阻断通过
  - 缺少字段时默认按 30 秒计算图片数量范围
- 新增动态图片数量范围：
  - min_images_for_duration = ceil(target_duration_seconds / 6)
  - max_images_for_duration = floor(target_duration_seconds / 3)
  - effective_min_images = max(6, min_images_for_duration)
- 新增 issue：
  - missing_target_duration_seconds：warning
  - invalid_target_duration_seconds：error
  - too_few_images_for_target_duration：error
  - too_many_images_for_target_duration：warning
- 当前边界：
  - 只改 validator 相关代码和文档
  - 不修改 preflight/checklist 逻辑
  - 不修改 MoneyPrinterTurbo 原业务代码

## Step 2-2 preflight 目标时长计算

- 当前目标：
  - preflight 读取 `target_duration_seconds`
  - 缺少字段时复用 validator warning，并默认按 30 秒处理
  - 根据目标时长和图片数量动态推荐 `video_clip_duration`
  - 输出图片总覆盖时长和旁白安全字数上限
- 动态计算：
  - raw_clip_duration = ceil(target_duration_seconds / image_count)
  - recommended_clip_duration = clamp(raw_clip_duration, 3, 6)
  - total_image_duration = image_count * recommended_clip_duration
  - will_loop = total_image_duration < max(target_duration_seconds, estimated_narration_seconds)
- 新增旁白上限：
  - narration_safe_seconds = target_duration_seconds - 3
  - narration_max_cjk_chars = floor(narration_safe_seconds * 4.0)
- 新增 warning：
  - narration_too_long_for_target_duration
  - image_duration_shorter_than_target_duration
  - image_duration_shorter_than_narration
- 当前边界：
  - 不修改 validator.py
  - 不修改 webui_checklist.py
  - 不修改 MoneyPrinterTurbo 原业务代码

## Step 2-3 checklist 目标时长展示

- 当前目标：
  - checklist 读取 `timing.target_duration_seconds`
  - 展示当前图片数量
  - 展示推荐 `video_clip_duration`
  - 展示图片总覆盖时长
  - 展示旁白安全时长和最大中文字符数
  - 强化 WebUI 最终 `video_script` 文案一致性提示
- 向后兼容：
  - 旧 report 缺少新增字段时不崩溃
  - 缺少字段显示“未提供”
  - 图片总覆盖时长可回退为图片数量 * 推荐时长
- 当前边界：
  - 不修改 validator.py
  - 不修改 preflight.py
  - 不修改 models.py
  - 不修改 MoneyPrinterTurbo 原业务代码

## Step 2-4 WebUI 餐厅视频模式

- 当前目标：
  - 不再只依赖外部 preflight/checklist
  - 在 WebUI 中直接加入餐厅视频模式
  - 让用户选择目标视频时长：30、40、50、60 秒
  - 根据目标时长、上传图片数量和文案长度给出提示和拦截
- 当前状态：
  - 已实现，待 WebUI 手动复测
  - 本次未启动新的 WebUI 进程
- 已加入 WebUI 控件：
  - 餐厅视频模式默认开启
  - 页面隐藏餐厅视频模式开关
  - 目标视频时长移动到左侧文案设置区域的视频主题下方
  - 脚本语言选择隐藏，默认使用中文 zh-CN
- 餐厅模式下隐藏/锁定通用参数：
  - 视频来源固定为 local / 本地文件
  - 视频拼接模式固定为 sequential / 顺序拼接
  - 同时生成视频数量固定为 1 条
  - 视频片段最大时长不再手动选择，改为根据目标时长和图片数量动态计算
- 餐厅模式规则：
  - 仅在 Local file / 本地文件素材下做第一版检查
  - 图片数量范围：min=max(6, ceil(target_duration_seconds / 6))，max=floor(target_duration_seconds / 3)
  - 图片少于最低要求时阻止生成
  - 图片多于建议上限时 warning，不阻止生成
  - 推荐 video_clip_duration = clamp(ceil(target_duration_seconds / image_count), 3, 6)
  - 文案中文字符范围：floor((target_duration_seconds - 6) * 4.0) 到 floor((target_duration_seconds - 3) * 4.0)
  - 文案偏短 warning：可能导致视频提前结束，部分图片无法出现
  - 文案偏长 warning：可能导致图片重复播放
- 生成前兜底：
  - 餐厅模式开启时再次强制写入 restaurant_mode=True
  - 再次强制写入 video_language=zh-CN
  - 餐厅模式开启时再次强制写入 video_source=local
  - 再次强制写入 video_concat_mode=sequential
  - 再次强制写入 video_count=1
  - 如果已有图片，重新计算并写入 video_clip_duration
- 当前边界：
  - 未修改 app/services/video.py
  - 未修改 TTS、字幕、ffmpeg 合成核心
  - 非餐厅模式默认关闭，尽量保持原 WebUI 行为不变

## Step 2-5 餐厅模式 AI 文案长度约束

- 当前问题：
  - 餐厅模式下点击 AI 自动生成视频文案和关键词时，生成文案可能不遵守目标时长对应的中文字符范围
  - 例如目标 40 秒建议 136-148 个中文字符，但 AI 可能生成超过上限的文案
- 已调整：
  - 餐厅模式下调用 AI 生成视频文案前，会把目标视频时长写入 prompt
  - 会把建议中文旁白长度范围写入 prompt
  - prompt 明确要求只输出可直接用于视频旁白的文案
  - prompt 明确要求不要输出分镜编号或解释
  - 页面在 AI 生成按钮附近显示当前目标时长对应的建议中文字符范围
- 保持不变：
  - 关键词生成仍沿用原逻辑
  - 生成后仍保留文案偏短/偏长 warning
  - 未修改 app/services/video.py
  - 未修改 TTS、字幕、ffmpeg 合成核心

## Step 2-6 餐厅默认流程页面精简

- 当前目标：
  - 进一步精简餐厅视频默认流程页面
  - 将用户必须操作的内容集中到左侧
  - 减少右侧固定参数说明占用空间
  - 提高 AI 自动生成文案落入目标字数范围的稳定性
- 页面调整：
  - 隐藏右侧固定说明：视频来源、本地文件固定
  - 隐藏右侧固定说明：视频拼接模式、顺序拼接固定
  - 隐藏右侧固定说明：同时生成视频数量、1 条固定
  - 保留上传本地文件入口
  - 视频比例移动到左侧目标视频时长下方
  - 视频比例仍写入 params.video_aspect
- AI 文案生成调整：
  - 首次生成后统计中文字符数
  - 如果偏短，自动进行一次扩写
  - 如果偏长，自动进行一次压缩
  - 二次修正只执行一次，避免无限循环
  - 二次修正后仍不在推荐范围内时，提示用户手动微调
  - 关键词生成仍基于最终文案沿用原逻辑
- 当前边界：
  - 未修改 app/services/video.py
  - 未修改 app/services/voice.py
  - 未修改 app/services/subtitle.py
  - 未修改 TTS、字幕、ffmpeg 合成核心

## Step 2-7 AI 文案长度程序级兜底

- 当前问题：
  - 40、50、60 秒目标下，AI 文案即使经过 prompt 约束和一次 AI 二次修正，仍可能普遍偏短
  - 仅依赖 prompt 或 AI 自我修正不能稳定满足目标中文字符范围
- 已调整：
  - AI 二次修正后增加程序级本地兜底
  - 文案偏短时，使用本地餐厅宣传模板句自动补足
  - 文案偏长时，按中文标点进行句子级压缩
  - 本地兜底不调用外部 API
  - 关键词生成基于最终修正后的文案
- 保持不变：
  - 用户手动编辑的视频文案不会被强制改写
  - 手动文案仍只显示偏短/偏长 warning
  - 未修改 app/services/video.py
  - 未修改 app/services/voice.py
  - 未修改 app/services/subtitle.py
  - 未修改 TTS、字幕、ffmpeg 合成核心

## Step 2-8 视频文案字数硬限制

- 当前目标：
  - 餐厅默认流程中，视频文案必须严格落入目标时长对应的中文字符范围
  - 生成按钮只有在文案字数和图片数量都符合要求时才可点击
- 已调整：
  - 视频文案输入框下方显示当前中文字符数和推荐范围
  - 目标视频时长切换后，推荐字数范围自动切换
  - 文案超过最大中文字符数时自动截断到上限内
  - 文案低于最小中文字符数时显示还差多少字
  - 生成按钮基于文案字数和图片数量启用/禁用
  - 生成前仍保留最终兜底检查，避免异常状态下调用生成任务
- AI 文案生成：
  - AI 生成和二次修正后继续进入本地字数归一化
  - 最终写入文案框的内容也会经过最大字数截断
  - 关键词生成仍基于最终文案
- 当前边界：
  - 未修改 app/services/video.py
  - 未修改 app/services/voice.py
  - 未修改 app/services/subtitle.py
  - 未修改 TTS、字幕、ffmpeg 合成核心

## Step 2-9 视频比例布局调整

- 当前目标：
  - 简化左侧文案设置区域
  - 将视频比例移动到中间列素材上传区域，靠近本地素材相关操作
- 已调整：
  - 左侧文案设置区域不再显示视频比例
  - 中间列餐厅默认流程中，视频比例显示在上传本地文件模块上方
  - 视频比例选项保持竖屏 9:16 和横屏 16:9
  - 继续写入原字段 `params.video_aspect`
- 当前边界：
  - 未修改 app/models/schema.py
  - 未修改 app/services/video.py
  - 未修改 app/services/voice.py
  - 未修改 app/services/subtitle.py
  - 未修改 TTS、字幕、ffmpeg 合成核心

## Step 2-10 Streamlit Clear caches 弹窗处理

- 当前问题：
  - 用户反馈在 WebUI 执行复制操作时会弹出 `Clear caches` 窗口
- 定位结论：
  - 未发现项目自定义 `Clear caches` 文案
  - 未发现项目自定义 clipboard / copy JS 事件绑定
  - 最可能来源是 Streamlit 内置菜单或 toolbar
- 已调整：
  - `st.set_page_config(...)` 中隐藏 Streamlit 默认菜单项
  - 增加最小 CSS 隐藏 Streamlit 内置菜单、toolbar、Deploy 按钮和状态入口
- 当前边界：
  - 不影响页面主体功能
  - 不影响上传本地文件
  - 不影响餐厅默认流程参数
  - 未修改 app/services/video.py
  - 未修改 TTS、字幕、ffmpeg 合成核心

## Step 2-11 左侧文案设置区域继续精简

- 当前目标：
  - 减少餐厅默认流程左侧文案设置区域的非必要控件
  - 让用户只处理主题、目标时长、AI 文案、文案正文和关键词
- 已调整：
  - 隐藏 `脚本语言：中文（餐厅视频流程默认）` 提示
  - 隐藏 `高级脚本设置` 模块
  - 后台仍默认写入 `video_language=zh-CN`
  - AI 文案生成仍使用默认段落数和默认系统设置
- 当前边界：
  - 不影响 AI 生成视频文案按钮
  - 不影响视频文案输入框
  - 不影响视频关键词输入框
  - 未修改 app/models/schema.py
  - 未修改 app/services/video.py
  - 未修改 TTS、字幕、ffmpeg 合成核心

## Step 2-12 中间列提示继续精简

- 当前目标：
  - 减少中间列素材上传区域的解释型文字
  - 保留必要错误和阻止信息
- 已调整：
  - 中间列不再显示详细旁白字数范围
  - 中间列不再显示当前文案中文字符数
  - 中间列不再显示 `视频片段最大时长不是最终视频总时长` 的解释说明
  - 文案字数不合格时仍显示简短提示
- 保持不变：
  - 底层字数范围计算仍保留
  - 超长自动截断仍保留
  - 低于最小字数时按钮禁用/阻止仍保留
  - 图片数量不足拦截仍保留
  - 未修改 app/models/schema.py
  - 未修改 app/services/video.py
  - 未修改 TTS、字幕、ffmpeg 合成核心

## Step 2-13 视频文案输入态自动截断

- 当前目标：
  - 修复视频文案输入框只提示不够实时的问题
  - 让超出最大中文字符数的内容不再作为可生成文案进入后端
- 已调整：
  - 视频文案输入框绑定独立 session key `video_script_input`
  - 后端通过 `on_change` 统计 CJK 中文字符数，作为兜底校验
  - 超过当前目标时长最大字数时，兜底截断后同步写回 `video_script`
  - 字数显示基于截断后的最终文案
- 保持不变：
  - 低于最小字数时仍禁用/阻止生成
  - AI 自动生成文案仍经过最大字数限制
  - 未修改 app/models/schema.py
  - 未修改 app/services/video.py
  - 未修改 TTS、字幕、ffmpeg 合成核心

## Step 2-14 视频文案微博式输入框限制

- 当前目标：
  - 将视频文案字数限制从 `输入后 rerun 截断` 升级为更接近新浪微博的输入体验
  - 达到最大中文字符数后，继续输入中文不再进入输入框
  - 粘贴超长内容时，只接收允许范围内的部分
- 已调整：
  - 保留 Streamlit 原生 `st.text_area`，确保值仍进入 `video_script_input` / `params.video_script`
  - 使用 `st.components.v1.html` 注入最小前端 JS，不新增依赖
  - 前端监听 `beforeinput`，在候选文本超过最大 CJK 字符数时阻止继续输入
  - 前端监听 `paste`，粘贴超长文案时只保留不超过最大 CJK 字符数的部分
  - 前端监听 `input`，作为浏览器端安全兜底并实时更新字数状态
  - 字数提示显示 `还差 X 字`、`还可输入 Y 字`、`已达上限`
  - 后端仍保留最大字数兜底、最小字数阻止生成和图片数量阻止生成
- 当前边界：
  - 不新增 Streamlit custom component 依赖
  - 不修改 app/models/schema.py
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 TTS、字幕、ffmpeg 合成核心

## Step 2-15 Clear caches 弹窗再次处理

- 当前问题：
  - 用户反馈 WebUI 中执行复制操作时仍会弹出 `Clear caches` 窗口
  - 这是当前体验阻塞问题，优先处理
- 定位结论：
  - 未发现项目自定义 `Clear caches` 文案或按钮
  - 未发现项目自定义 copy / clipboard 复制事件绑定
  - 当前 `clipboardData` 仅用于视频文案输入框的 paste 限制，不监听 copy，不会主动打开弹窗
  - 最可能来源仍是 Streamlit 内置 header / toolbar / menu 入口
- 已调整：
  - 在 `webui/Main.py` 中加固 Streamlit 内置菜单隐藏 CSS
  - 隐藏 `#MainMenu`、`stMainMenu`、`stHeader`、`stToolbar`、`stDeployButton`、`stAppDeployButton`
  - 隐藏 `.stDeployButton`、`header` 以及常见 Main menu / Deploy 按钮入口
- 当前边界：
  - 保留浏览器正常复制能力
  - 不影响页面主体、上传文件、生成按钮和餐厅默认流程
  - 不修改 app/models/schema.py
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 TTS、字幕、ffmpeg 合成核心

## Step 2-16 AI 生成按钮文案精简

- 当前目标：
  - 精简左侧 AI 生成按钮显示文案
  - 将 `点击使用AI根据主题生成视频文案和视频关键词` 类似长文案统一改为 `AI生成视频文案`
- 已调整：
  - 修改中文 i18n 文案 `Generate Video Script and Keywords`
  - 按钮 key 和调用逻辑保持不变
  - AI 仍按当前逻辑根据主题生成视频文案
  - 如果当前逻辑生成关键词，则继续保持原行为
  - 餐厅模式下字数约束、二次修正和本地兜底逻辑保持不变
- 当前边界：
  - 不修改 webui/Main.py 的按钮功能逻辑
  - 不修改 app/models/schema.py
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 TTS、字幕、ffmpeg 合成核心

## Step 2-17 AI 文案与关键词前台流程精简

- 当前目标：
  - 左侧前台只保留一个 `AI生成视频文案` 按钮
  - 点击后生成视频文案，并自动根据最终视频文案生成关键词
  - 隐藏独立关键词生成按钮、视频关键词标题和视频关键词输入框
- 已调整：
  - 餐厅默认流程下不再显示 `点击使用AI根据文案生成视频关键词` 按钮
  - 餐厅默认流程下不再显示视频关键词输入框
  - `AI生成视频文案` 按钮仍先生成视频文案
  - 文案经过餐厅模式字数约束、二次修正和本地兜底后，再用于关键词生成
  - 自动生成的关键词仍写入 `params.video_terms`
  - 如果关键词生成失败，只提示 warning，并使用本地默认关键词兜底
  - 手动修改文案后，不自动调用关键词 API
  - 点击生成视频时，如果关键词为空，使用本地默认关键词兜底，避免后端再调用关键词 API
- 当前边界：
  - 不删除 `params.video_terms` 字段
  - 不修改 app/models/schema.py
  - 不修改 app/services/task.py
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 TTS、字幕、ffmpeg 合成核心

## Step 2-18 Clear caches 弹窗强制抑制

- 当前问题：
  - 用户反馈 WebUI 中复制文本时仍反复弹出 `Clear caches` 窗口
  - 该问题作为当前体验阻塞问题优先处理
- 定位结论：
  - 未发现项目自定义 `Clear caches` 文案或按钮
  - 未发现项目自定义 copy / clipboard 复制事件绑定
  - 当前自定义 `clipboardData` 仅用于视频文案输入框的 paste 限制，不监听 copy
  - 更可能是 Streamlit 内置 toolbar / menu / cache 弹窗
- 已调整：
  - 新增集中 helper `hide_streamlit_dev_chrome_and_cache_popup()`
  - 在 `st.set_page_config(...)` 后立即调用
  - 整合并加固 Streamlit 顶部菜单 / toolbar / deploy / status 隐藏 CSS
  - 注入最小 JS，使用 `MutationObserver` 监听 DOM
  - 当页面出现 `Clear cache`、`Clear caches`、`Clear Cache`、`Clear Caches`、`清除缓存` 文案时，自动隐藏最近的菜单、弹窗或 popover 容器
- 当前边界：
  - 不拦截 Ctrl+C / Cmd+C
  - 不阻止浏览器正常复制文本
  - 不删除 `st.cache_data` 或其他缓存机制
  - 不影响上传文件、生成按钮和餐厅默认流程
  - 不修改 app/models/schema.py
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 TTS、字幕、ffmpeg 合成核心

## Step 2-19 WebUI 品牌显示调整

- 当前目标：
  - 将 WebUI 页面左上角显示从 `MoneyPrinterTurbo v1.2.9` 调整为 `TwinkleBite AI`
  - 仅调整 WebUI 品牌显示文案
- 已调整：
  - `webui/Main.py` 中浏览器页面标题改为 `TwinkleBite AI`
  - `webui/Main.py` 中左上角 `st.title(...)` 改为 `TwinkleBite AI`
  - 页面不再显示版本号后缀
- 当前边界：
  - 不全局替换 `MoneyPrinterTurbo`
  - 不修改项目包名
  - 不修改 Git 仓库名
  - 不修改历史文档中的原项目说明
  - 不修改 app/models/schema.py
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 TTS、字幕、ffmpeg 合成核心

## Step 2-20 Cmd+C 页面空白稳定性修复

- 当前问题：
  - 用户反馈 WebUI 中连按 `Cmd+C` 复制会造成页面空白
  - 最近加入的 `Clear caches` 抑制逻辑包含全局 `MutationObserver` 和 DOM 隐藏逻辑，存在误伤 Streamlit 页面主体的风险
- 已调整：
  - 移除 `Clear caches` 全局 `MutationObserver` / 弹窗 DOM 删除逻辑
  - 不再根据 `Clear cache(s)` 文案扫描和隐藏 `div`、`section`、`modal`、`popover` 等容器
  - 保留最小 Streamlit 菜单 CSS 隐藏，仅隐藏 `#MainMenu`、`[data-testid="stToolbar"]`、`[data-testid="stStatusWidget"]` 和 `.stDeployButton`
  - 不再隐藏整个 `header`
  - 不再隐藏 `[data-testid="stDecoration"]`、`[data-testid="baseButton-header"]` 等高风险选择器
- 当前边界：
  - 页面稳定性优先于强制抑制 `Clear caches`
  - 不拦截 `Cmd+C` / `Ctrl+C`
  - 不监听 `copy` 事件
  - 不修改 app/models/schema.py
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 TTS、字幕、ffmpeg 合成核心

## Step 2-21 Clear caches 快捷键精确拦截

- 当前问题：
  - 移除全局 `MutationObserver` 后，页面空白问题已缓解
  - 用户反馈连按复制仍会触发 `Clear caches` 弹窗
- 已调整：
  - 不恢复全局 DOM 扫描
  - 新增精确 keyboard guard
  - 普通 `Cmd+C` / `Ctrl+C` 不拦截，保留正常复制
  - 仅在非输入区域拦截带 `Shift` 或 `Alt` 的 C 组合键，例如 `Cmd+Shift+C`、`Ctrl+Shift+C`、`Cmd+Alt+C`、`Ctrl+Alt+C`
  - 在 `input`、`textarea`、`contenteditable` 中绝不拦截
  - 继续保留最小 Streamlit 菜单 / toolbar CSS 隐藏
- 当前边界：
  - 不使用全局 `MutationObserver`
  - 不扫描或删除 `modal`、`popover`、`div`、`section` 等页面容器
  - 不监听 `copy` 事件
  - 不修改 app/models/schema.py
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 TTS、字幕、ffmpeg 合成核心

## Step 2-22 Clear caches 原生弹窗精确抑制

- 当前问题：
  - 用户截图确认普通 `Cmd+C` 连按后仍会触发 Streamlit 原生 `Clear caches` dialog
  - `keyboard guard` 不足以彻底阻止该弹窗
- 已调整：
  - 保留最小 Streamlit toolbar / menu CSS
  - 保留普通 `Cmd+C` / `Ctrl+C` 复制能力
  - 新增精确 `Clear caches` dialog guard
  - 使用 `MutationObserver` 仅监听 dialog / modal 候选，不扫描全页面 `div` / `section`
  - 候选范围限制为 `[role="dialog"]`、`[data-baseweb="modal"]`、`[data-testid="stModal"]`、`[data-testid*="Modal"]`
  - 只有候选弹窗文本同时包含 `Clear caches` 和缓存确认文案时才处理
  - 优先点击 `Cancel` 或关闭按钮；找不到按钮时才隐藏该 dialog
- 当前边界：
  - 不恢复全局 DOM 扫描
  - 不扫描或隐藏全页面 `div`、`section`、`header`、app 容器
  - 不拦截普通复制
  - 不修改 app/models/schema.py
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 TTS、字幕、ffmpeg 合成核心

## Step 2-23 WebUI 餐厅默认流程收口

- 当前状态：
  - 本轮 WebUI 餐厅默认流程改造已完成，准备提交
  - 用户已确认 `Clear caches` 复制阻塞问题已解决
  - 页面不再因复制操作出现阻塞问题
- 本轮核心结果：
  - WebUI 品牌显示调整为 `TwinkleBite AI`
  - 餐厅视频流程默认开启
  - 目标视频时长支持 30 / 40 / 50 / 60 秒
  - 视频来源固定本地文件并隐藏通用选择
  - 拼接模式固定顺序拼接并隐藏通用选择
  - 视频片段时长根据目标时长和图片数量自动计算
  - 同时生成视频数量固定 1
  - 视频比例移动到中间列上传本地文件模块上方
  - 左侧隐藏脚本语言、高级脚本设置和独立关键词输入
  - 前台只保留 `AI生成视频文案` 一个 AI 按钮
  - AI 生成文案后自动根据最终文案生成关键词，并写入 `params.video_terms`
  - 文案中文字符数成为硬性生成条件
  - 图片数量不足时阻止生成
  - 精确抑制 Streamlit 原生 `Clear caches` dialog，避免复制体验阻塞
- 当前边界：
  - 未修改 app/services/video.py
  - 未修改 app/services/voice.py
  - 未修改 app/services/subtitle.py
  - 未修改 config.toml
  - 未修改 restaurant_engine/
  - 未修改 storage/
  - 未修改 TTS、字幕、ffmpeg 视频合成核心
  - 未提交生成视频、音频、字幕、报告或缓存文件

## Step 2-24 TwinkleBite AI WebUI 初版里程碑

- 当前阶段里程碑：
  - `TwinkleBite AI` 默认餐厅视频 WebUI 初版已完成并提交
  - 提交：`f287eb85c5131dc305bf6e5d651d4b2161e3839a`
  - 提交说明：`feat: add default restaurant video WebUI workflow`
- 已实现能力：
  - WebUI 品牌显示为 `TwinkleBite AI`
  - 餐厅视频流程默认开启
  - 目标视频时长支持 30 / 40 / 50 / 60 秒
  - 视频来源固定本地文件
  - 拼接模式固定顺序拼接
  - 视频片段时长按目标时长和图片数量自动计算
  - 同时生成视频数量固定 1
  - 视频比例移至上传本地文件模块上方
  - 隐藏脚本语言、高级脚本设置、关键词输入框、独立关键词生成按钮
  - 只保留 `AI生成视频文案` 按钮
  - AI 生成视频文案后自动生成关键词
  - 视频文案字数按目标时长硬限制
  - 图片数量不足会阻止生成
  - `Clear caches` 复制弹窗问题已处理
- 当前边界：
  - 未修改 app/services/video.py
  - 未修改 app/services/voice.py
  - 未修改 app/services/subtitle.py
  - 未修改 config.toml
  - 未提交 storage/、.pyc、__pycache__/、生成产物
- 下一步建议：
  - 尽快 push 当前分支到远程仓库
  - 用至少 2-3 个真实餐厅样本做完整生成测试
  - 记录每个样本的视频质量、图片是否全部出现、是否重复、字幕/语音同步情况
  - 暂停继续堆 UI 小改动，优先做稳定性测试

## 当前修复：餐厅模式每图时长分配

- 背景：
  - `hotpot_001` 30 秒 / 8 张图复测时，最终视频约 28 秒，第 8 张图片未出现。
  - 页面顺序、字幕、语音、BGM 正常，主要问题是图片覆盖时长与最终合成停止条件不一致。
- 结论：
  - 单一 `video_clip_duration` 不足以表达 30 秒 / 8 张图这类不能整除的场景。
  - 餐厅模式需要为每张图片生成整数秒时长列表，并让列表总和等于目标视频时长。
- 当前实施方向：
  - 新增 `video_clip_durations` 可选参数。
  - WebUI 餐厅模式按目标时长和图片数量生成 per-image duration。
  - 本地图片预处理按每张图对应时长生成素材视频。
  - 合成阶段收到完整 per-image duration 时，按时长列表总和覆盖目标时长，不再因音频较短提前丢掉尾部图片。
- 示例规则：
  - 30 秒 / 8 张图：`[4, 4, 3, 4, 4, 3, 4, 4]`
  - 30 秒 / 6 张图：`[5, 5, 5, 5, 5, 5]`
  - 40 秒 / 8 张图：`[5, 5, 5, 5, 5, 5, 5, 5]`
- 当前边界：
  - 未修改 TTS、字幕、BGM、语音服务。
  - 未修改配置文件。
  - 未提交生成产物。
  - 修复后需要重新启动 WebUI，并由用户手动复测 hotpot_001 Case A。

## 当前修复验证：Case A hotpot_001 通过

- Case A 初测问题：
  - `hotpot_001` 使用 30 秒目标时长和 8 张图片时，初测生成视频约 28 秒。
  - 第 8 张图片未出现。
  - 原因判断：旧逻辑仍按固定/最大片段时长计算，最终合成受音频时长提前停止影响。
- 已完成修复：
  - 新增 `video_clip_durations`。
  - 餐厅模式按目标总时长和图片数量生成整数秒片段列表。
  - 所有片段均为整数秒。
  - 所有片段总和等于目标时长。
  - 余数均匀分配。
  - `30 秒 / 8 张图 = 4, 4, 3, 4, 4, 3, 4, 4 秒`。
- 用户复测结果：
  - 页面显示整数片段列表：是。
  - 页面显示覆盖时长：30 秒。
  - 成片时长：30 秒。
  - 8 张图片全部出现：是。
  - 图片无重复：是。
  - 图片顺序正确：是。
  - 字幕出现且与语音同步：是。
  - BGM 正常：是。
  - 页面无报错：是。
- 当前结论：
  - Case A 通过。
  - 整数秒 per-image duration 修复有效，已解决第 8 张图片未出现的问题。

## 当前验证：Case B sichuan_001 通过

- 用户手动测试结果：
  - 样本：`sichuan_001`
  - 目标时长：30 秒
  - 图片数量：6 张
  - 页面显示整数片段列表：是。
  - 页面显示的片段列表：`5, 5, 5, 5, 5, 5 秒`。
  - 页面显示覆盖时长：30 秒。
  - 成片时长：30 秒。
  - 6 张图片全部出现：是。
  - 图片无重复：是。
  - 图片顺序正确：是。
  - 字幕出现且与语音同步：是。
  - BGM 正常：是。
  - 页面无报错：是。
- 当前结论：
  - Case B 通过。
  - 30 秒 / 6 张图片的整数秒片段分配正常，完整生成流程稳定。
- 当前已验证样本：
  - `hotpot_001`：30 秒 / 8 图，通过。
  - `sichuan_001`：30 秒 / 6 图，通过。
- 下一步建议：
  - 补充第三个真实餐厅样本，至少 8 张图片。
  - 测试 40 秒流程。

## 当前验证：Case C 40 秒真实餐厅样本通过

- 用户手动测试结果：
  - 样本：第三个真实餐厅样本，火锅店样本。
  - 目标时长：40 秒。
  - 图片数量：8 张。
  - 页面显示整数片段列表：是。
  - 页面显示的片段列表：`5, 5, 5, 5, 5, 5, 5, 5 秒`。
  - 页面显示覆盖时长：40 秒。
  - 成片时长：40 秒。
  - 8 张图片全部出现：是。
  - 图片无重复：是。
  - 图片顺序正确：是。
  - 字幕出现且与语音同步：是。
  - BGM 正常：是。
  - 页面无报错：是。
- 当前结论：
  - Case C 通过。
  - 40 秒 / 8 张图片流程稳定，整数秒片段分配正常。
- 当前多样本验证总结：
  - 30 秒 / 8 图：通过。
  - 30 秒 / 6 图：通过。
  - 40 秒 / 8 图：通过。
- 当前阶段结论：
  - `TwinkleBite AI` 餐厅视频默认 WebUI 主流程已完成 30 秒与 40 秒真实样本验证。
  - 整数秒图片片段分配逻辑通过多样本测试。
- 下一步建议：
  - 后续可继续测试 50 秒 / 10 图、60 秒 / 12 图。
  - 暂停继续改核心逻辑，优先沉淀使用说明和样本规范。

## 当前验证：50 秒与 60 秒流程通过

- 用户补充测试结果：
  - 50 秒 / 10 图：已测试，暂未发现问题。
  - 60 秒 / 12 图：已测试，暂未发现问题。
- 当前已完成验证矩阵：
  - 30 秒 / 8 图：通过。
  - 30 秒 / 6 图：通过。
  - 40 秒 / 8 图：通过。
  - 50 秒 / 10 图：通过，暂未发现问题。
  - 60 秒 / 12 图：通过，暂未发现问题。
- 当前结论：
  - `TwinkleBite AI` 餐厅视频 MVP 主流程已覆盖 30 / 40 / 50 / 60 秒目标时长。
  - 整数秒图片片段分配逻辑通过多时长、多图片数量测试。
  - 当前暂未发现新的主流程问题。
- 下一步建议：
  - 暂停继续改核心逻辑。
  - 后续可优化 WebUI 后台启动保活。
  - 后续可测试 AI 文案按钮外部 API 稳定性。
  - 后续可整理演示样本包。

## 当前补充：WebUI 后台启动脚本

- 本次目标：
  - 增加本机 macOS 后台启动、停止和状态检查能力。
  - 不修改 WebUI 功能逻辑。
  - 不修改视频生成核心。
- 新增脚本：
  - `scripts/twinkle_webui_start.sh`
  - `scripts/twinkle_webui_stop.sh`
  - `scripts/twinkle_webui_status.sh`
- 使用方式：
  - `scripts/twinkle_webui_start.sh`
  - `scripts/twinkle_webui_status.sh`
  - `scripts/twinkle_webui_stop.sh`
- 运行文件：
  - PID：`.runtime/twinkle_webui.pid`
  - 日志：`.runtime/twinkle_webui.log`
  - `.runtime/` 已加入 `.gitignore`，不进入 Git。
- 行为约束：
  - 如果端口 8501 已被占用，start 会拒绝启动，不会强杀。
  - stop 只使用普通 `kill` 温和停止，不默认 `kill -9`。
  - status 显示 PID、端口监听、WebUI URL 和最近日志。
- 用户手动验证结果：
  - start：成功。
  - 关闭终端后：WebUI 仍保持运行。
  - status：能看到 PID 正在运行、8501 正在监听。
  - stop：成功。
  - stop 后：PID file exists: no。
  - stop 后：8501 无 listener。

## 当前验证：AI 生成视频文案按钮初步通过

- 用户手动测试结果：
  - AI-A：30 秒，主题 `四川火锅宣传`，成功返回文案，实际中文字符数 102，推荐范围 96-108，合规，已自动填入视频文案框，页面/API 无报错。
  - AI-B：40 秒，主题 `重庆老火锅门店探店`，成功返回文案，实际中文字符数 148，推荐范围 136-148，合规，已自动填入视频文案框，页面/API 无报错。
  - AI-C：60 秒，主题 `川菜馆招牌菜推荐`，成功返回文案，实际中文字符数 226，推荐范围 216-228，合规，已自动填入视频文案框，页面/API 无报错。
- 当前结论：
  - `AI生成视频文案` 按钮外部 API 稳定性初步通过。
  - 字数控制和自动压缩/长度兜底逻辑有效。
  - 隐藏关键词流程未影响用户操作。
- 当前 MVP 已验证范围：
  - 30 / 40 / 50 / 60 秒视频主流程通过。
  - AI 文案按钮 30 / 40 / 60 秒通过。
- 后续建议：
  - 后续可补测 50 秒 AI 文案。
  - 后续可测试更多主题风格。
  - 暂停改核心逻辑。

## 当前阶段：WebUI 页面精简与样式清理

- 本轮目标：
  - 精简普通用户不需要看的技术提示和长说明。
  - 让页面更像餐厅短视频产品，而不是技术控制台。
- 本轮调整范围：
  - 精简 `视频主题`、`目标视频时长`、`视频文案` 等说明文案。
  - 保留 `AI生成视频文案` 按钮，并简化 AI 文案生成成功/校准提示。
  - 精简中间列图片展示时长说明。
  - 将 API Key 折叠入口文案简化为 `API Key 管理`。
- 当前边界：
  - 只调整 WebUI 展示文案和低风险说明文字。
  - 不修改视频生成核心。
  - 不修改整数秒片段分配逻辑。
  - 不修改后台脚本。
  - 不修改 TTS、字幕、BGM 逻辑。

## 当前补充：朗读声音选项精简

- WebUI 页面精简阶段继续推进。
- `朗读声音` 选项已在 WebUI 层过滤为 `zh-CN` 中文普通话声音。
- 默认声音优先使用 `zh-CN-XiaoxiaoNeural` 系列；如果不可用，则回退到第一个 `zh-CN` 声音。
- 若当前 TTS 配置找不到 `zh-CN` 声音，页面会提示检查 TTS 声音配置，不再默认展示非中文声音。
- 朗读声音下拉框用户可见标签已去掉 `zh-CN-` 前缀，例如 `zh-CN-Yunjian-Male` 显示为 `Yunjian-男声`。
- 朗读声音下拉框用户可见性别标签统一为 `男声` / `女声`，不再显示 `男性` / `女性`。
- 底层 TTS `voice_name` 保持原始完整值，不影响语音生成。
- `音频设置` 中的 TTS 服务器选择模块已隐藏，普通用户不再需要选择 TTS 服务。
- 底层仍沿用当前默认 TTS server 配置；配置无效时回退到 `azure-tts-v1`。
- `朗读音量`、`朗读速度`、`自定义音频文件` 模块已隐藏。
- 底层仍使用默认朗读音量 `1.0`、朗读速度 `1.0`，且不使用自定义音频文件。
- `朗读声音` 与背景音乐设置保留。
- `朗读声音` 字段已去掉与文案语言、API Key 相关的技术说明，只保留简洁标签。
- 背景音乐下拉框隐藏 `自定义背景音乐` 选项，普通用户只选择内置/随机/无背景音乐。
- 底层自定义 BGM 能力不删除，背景音乐音量设置保留。
- 浏览器确认发现 `背景音乐音量` 控件仍显示，本轮已隐藏该控件。
- 底层仍使用默认背景音乐音量 `0.2`，不影响背景音乐混音。
- 当前边界：
  - 未删除底层 TTS 多语言能力。
  - 未修改 `app/services/voice.py`。
  - 未修改视频生成核心。
  - 未修改后台脚本。

## 当前补充：背景音乐精选命名准备

- 开始整理 TwinkleBite AI 背景音乐精选名称。
- 当前先建立 BGM 试听清单和本机试听脚本。
- 新增文档：
  - `restaurant_docs/BGM_CATALOG.md`
- 新增试听脚本：
  - `scripts/twinkle_bgm_preview.sh`
- 当前边界：
  - 暂不修改 WebUI 背景音乐下拉框。
  - 暂不主观命名背景音乐。
  - 后续由用户试听后确认精选名称，再接入 WebUI。
  - 未修改视频生成核心。

## 当前补充：视频设置继续精简

- 继续精简 WebUI 视频设置。
- 餐厅默认流程中隐藏 `视频转场模式` 控件。
- 底层继续使用 `无转场`。
- 餐厅默认流程中隐藏 `高级视频设置` 模块。
- 底层继续沿用当前默认高级视频参数。
- 未上传图片时隐藏 `上传图片后自动计算每张图片展示时长` 蓝色提示。
- 上传图片后的片段分配显示、图片数量校验和生成前拦截保持不变。
- 当前边界：
  - 未修改 `app/services/video.py`。
  - 未修改 `app/services/task.py`。
  - 未修改视频生成核心。
  - 未修改后台脚本。

## 当前补充：字幕设置布局纠正

- 纠正字幕设置布局。
- `字幕设置` 应位于中间列 `音频设置` 下方，而不是图片数量信息下方。
- `字幕设置` 已从右侧独立列移除。
- 本轮只调整 WebUI 布局。
- 未修改 `app/services/subtitle.py`。
- 未修改字幕生成逻辑或视频生成核心。

## 当前补充：字幕设置继续精简

- 继续精简 WebUI 字幕设置。
- `字幕设置` 区域只保留 `启用字幕` 开关，其余样式控件隐藏。
- 底层使用默认字幕样式：
  - 字幕字体：`STHeitiMedium.ttc`
  - 字幕位置：底部
  - 字幕颜色：白色
  - 字号：`50`
  - 描边颜色：黑色
  - 描边粗细：`1.5`
  - 字幕背景：关闭
  - 圆角半透明字幕背景：关闭
- 用户取消 `启用字幕` 时，字幕仍会关闭。
- 未修改 `app/services/subtitle.py`。
- 未修改字幕生成逻辑或视频生成核心。

## 当前补充：视频片段明细展示隐藏

- 继续精简 WebUI 视频设置。
- 上传图片后隐藏以下展示：
  - 每张图片展示时长。
  - 预计图片总覆盖时长。
  - 自动分配展示时间说明。
- 继续保留目标时长建议图片数量和当前本地图片数量。
- 底层整数秒片段分配仍保留，并继续写入 `video_clip_durations`。
- 未修改 `app/services/video.py`。
- 未修改 `app/services/task.py`。
- 未修改 `app/models/schema.py`。
- 未修改视频生成核心。

## 当前补充：API Key 管理入口隐藏

- 继续精简 WebUI 页面。
- 当前餐厅 MVP 只使用本地上传图片，右侧 Pexels / Pixabay API Key 管理入口已从普通界面隐藏。
- 底层 API Key 管理逻辑和配置保留。
- 未删除已有 API Key。
- 未修改 `config.toml`。
- 未影响本地图片上传。
- 未影响 `AI生成视频文案` 按钮。
- 未修改视频生成核心。

## 当前补充：主页面两列布局

- 继续精简 WebUI 布局。
- 隐藏 API Key 管理后，移除右侧空白列。
- 主页面改为两列布局：
  - 左列：文案设置。
  - 右列：视频设置、音频设置、字幕设置。
- 右列顺序保持为 `视频设置` → `音频设置` → `字幕设置`。
- 本轮只调整页面布局。
- 未修改本地上传、目标时长、字数校验或 AI 文案按钮逻辑。
- 未修改视频生成核心。

## 第 2 阶段：restaurant_engine Pipeline 骨架

- 开始进入 `restaurant_engine` Pipeline 骨架阶段。
- 当前 MoneyPrinterTurbo 仅作为第一阶段生成能力验证仓库。
- 新增能力优先放在 `restaurant_engine/`，不继续扩展 MoneyPrinterTurbo WebUI 作为正式产品。
- 本阶段已实现最小 pipeline 骨架：
  - 读取仓库外 `project.json`。
  - 调用已有 validator 校验输入。
  - 扫描本地 `images` 目录。
  - 创建样本项目 `output/` 目录。
  - 输出 mock `storyboard.json`。
  - 输出 `pipeline_report.json`。
- 当前边界：
  - 不生成视频。
  - 不生成封面。
  - 不调用 DeepSeek。
  - 不调用 TTS。
  - 不调用 AI 图生视频。
  - 不调用外部 API。
  - 不修改 WebUI。
  - 不修改 MoneyPrinterTurbo 原有业务代码。
  - 不修改视频生成核心。

## 第 2 阶段补充：DeepSeek planner 安全接入

- DeepSeek 接入审查已完成。
- `restaurant_engine` 开始接入 DeepSeek storyboard planner。
- pipeline 默认 planner 仍为 `mock`，默认不调用外部 API。
- DeepSeek planner 必须显式使用：
  - `--planner deepseek`
  - `--allow-external-api`
- 如果只指定 `--planner deepseek`，但未允许外部 API：
  - 不调用 DeepSeek。
  - `pipeline_report.json` 写入 `ok=false`。
  - `external_api_called=false`。
- 新增敏感文件 ignore 规则，覆盖 `.env`、key、pem、secret、token 等常见本地凭证文件。
- 当前边界：
  - 本轮实现不主动调用外部 API。
  - 未修改 WebUI。
  - 未修改 `app/services/llm.py`。
  - 未修改视频生成核心。

## 第 2 阶段验证：DeepSeek planner 真实调用

- DeepSeek planner 真实调用已通过首次验证。
- 本次仅执行用户授权的显式命令：
  - `--planner deepseek`
  - `--allow-external-api`
- DeepSeek planner 已能生成真实 `storyboard.json`。
- `pipeline_report.json` 关键结果：
  - `ok=true`
  - `planner=deepseek`
  - `external_api_allowed=true`
  - `external_api_called=true`
  - `validation_passed=true`
- 样本图片数量与 scene 数量一致：
  - `image_count=8`
  - `scene_count=8`
- scene 顺序与图片文件名顺序一致。
- storyboard 包含真实中文餐厅宣传旁白摘要，例如“正宗川味，太上头！”。
- 安全检查：
  - 未发现 API Key 写入 `pipeline_report.json` 或 `storyboard.json`。
  - 未发现 `sk-`、`api_key`、`Authorization`、`Bearer` 写入输出文件。
  - 仓库内未误生成 `pipeline_report.json` 或 `storyboard.json`。
- 当前边界：
  - 未生成视频。
  - 未修改代码。
  - 未修改 WebUI。
  - 未修改视频生成核心。
- 当前非阻塞问题：
  - DeepSeek 返回的 `total duration field` 为 `24`，8 个 scene 每个 3 秒。
  - 后续进入真实视频链路前，需要增强 `target_duration_seconds` 时长约束，或由后续时长分配模块覆盖。

## 第 2 阶段补充：Storyboard 时长约束增强

- 开始增强 DeepSeek planner 和 mock planner 的 scene 时长对齐逻辑。
- 新增本地整数秒 scene duration 分配规则：
  - `duration_seconds` 全部为整数。
  - scene 数量等于图片数量。
  - scene duration 总和等于 `target_duration_seconds`。
  - 缺少 `target_duration_seconds` 时沿用 validator 默认 `30` 秒。
- 当前关键样例：
  - `30 秒 / 8 图` → `4, 4, 3, 4, 4, 3, 4, 4`。
  - `30 秒 / 6 图` → `5, 5, 5, 5, 5, 5`。
  - `40 秒 / 8 图` → `5, 5, 5, 5, 5, 5, 5, 5`。
  - `50 秒 / 10 图` → `5, 5, 5, 5, 5, 5, 5, 5, 5, 5`。
  - `60 秒 / 12 图` → `5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5`。
- mock storyboard 不再使用固定 `5` 秒时长，改为使用目标时长分配结果。
- DeepSeek planner prompt 会包含目标时长、图片数量和要求的 scene duration 列表。
- DeepSeek 返回后，本地 pipeline 会覆盖 scene duration，避免外部 planner 返回 `24` 秒等与目标不一致的问题进入后续链路。
- DeepSeek scene 数量或图片顺序不匹配仍会失败。
- 本轮不调用 DeepSeek。
- 本轮不调用任何外部 API。
- 本轮不生成视频。
- 未修改 WebUI、`app/`、`config.toml` 或 MoneyPrinterTurbo 视频生成核心。

## 第 2 阶段验证：DeepSeek planner 时长对齐真实测试

- DeepSeek planner 时长对齐真实测试已通过。
- 本次仅记录用户授权的真实 DeepSeek planner pipeline 测试结果，不再次调用外部 API。
- DeepSeek planner 在真实 API 返回后，scene duration 已由本地逻辑强制归一化。
- 关键结果：
  - `pipeline_report.ok=true`
  - `planner=deepseek`
  - `external_api_allowed=true`
  - `external_api_called=true`
  - `target_duration_seconds=30`
  - `scene_durations=[4, 4, 3, 4, 4, 3, 4, 4]`
  - `storyboard total_duration_seconds=30`
  - `duration_sum=30`
  - `image_count=8`
  - `scene_count=8`
- scene 顺序与图片文件名排序完全一致。
- storyboard 包含真实中文餐厅宣传文案摘要，例如“正宗川味太上头，麻辣鲜香，一吃就停不下来！”。
- 未出现 mock 占位文案；兼容字段保留，但内容为真实文案。
- 安全检查：
  - 未发现 API Key 写入 `pipeline_report.json` 或 `storyboard.json`。
  - 未发现 `sk-`、`api_key`、`Authorization`、`Bearer` 写入输出文件。
  - 仓库内未误生成 `pipeline_report.json` 或 `storyboard.json`。
- 当前边界：
  - 未生成视频。
  - 未修改代码。
  - 未修改 WebUI。
  - 未修改 `app/`。
  - 未修改 `config.toml`。
- 当前阻塞问题：无。
- 当前非阻塞问题：
  - 系统 `python3` 缺少项目依赖，本次实际使用项目 `.venv` Python 执行同等 pipeline 命令。

## 第 2 阶段补充：Storyboard Contract 强化

- 开始实现 storyboard contract 校验。
- 该校验是进入 TTS、图生视频和视频合成前的结构门禁。
- 新增校验内容：
  - `scenes` 必须存在且是 list。
  - scene 数量必须等于本地图片数量。
  - scene 顺序必须与图片文件名排序一致。
  - scene 必填字段完整：`index`、`role`、`image_name`、`image_path`、`duration_seconds`、`narration` 或 `mock_narration`。
  - `index` 必须从 `1` 开始连续递增。
  - `image_path` 文件名必须与 `image_name` 一致。
  - `duration_seconds` 必须是正整数。
  - scene duration 总和必须等于 `target_duration_seconds`。
  - `storyboard.total_duration_seconds` 必须等于 `target_duration_seconds`。
  - `project_id` 和 `version` 必须存在。
  - narration 文本不能为空。
  - mock planner 中 mock 占位文案只记 warning。
  - DeepSeek planner 中 mock 占位文案记 error。
- pipeline 新增 `validate_storyboard_contract` step。
- `pipeline_report.json` 新增 contract 结果字段：
  - `storyboard_contract_passed`
  - `storyboard_contract_errors`
  - `storyboard_contract_warnings`
  - `duration_sum`
- 当前边界：
  - 本轮不调用 DeepSeek。
  - 本轮不调用任何外部 API。
  - 本轮不生成视频。
  - 未修改 WebUI。
  - 未修改 `app/`。
  - 未修改 `config.toml`。
  - 未修改 MoneyPrinterTurbo 视频生成核心。

## 第 2 阶段补充：Storyboard Quality Contract 增强

- 开始实现 storyboard quality contract。
- 目标是在进入 TTS、图生视频和视频合成前，进一步约束 storyboard 内容质量。
- 本轮增强内容：
  - mock planner 不再输出简单英文 `Mock narration...`。
  - mock planner 改为输出中文餐厅宣传片草稿文案。
  - 每个 scene 增加：
    - `visual_instruction`
    - `selling_point`
    - `transition_hint`
  - DeepSeek prompt 要求返回上述质量字段。
  - DeepSeek 返回后保留上述字段进入 storyboard。
  - pipeline 新增 `validate_storyboard_quality` step。
  - `pipeline_report.json` 新增：
    - `storyboard_quality_passed`
    - `storyboard_quality_errors`
    - `storyboard_quality_warnings`
- quality contract 校验内容：
  - narration 不能为空。
  - narration 必须包含中文宣传文案。
  - narration 中文字符数不能过短或过长。
  - scene narration 不能重复。
  - `visual_instruction`、`selling_point`、`transition_hint` 必须存在且非空。
  - 不允许明显 mock / placeholder 文案。
  - DeepSeek planner 不允许 mock / placeholder 文案。
- 当前边界：
  - 本轮不调用 DeepSeek。
  - 本轮不调用任何外部 API。
  - 本轮不生成视频。
  - 未修改 WebUI。
  - 未修改 `app/`。
  - 未修改 `config.toml`。
  - 未修改 MoneyPrinterTurbo 视频生成核心。

## 第 2 阶段修正：Storyboard Quality Contract 阈值调整

- 真实 DeepSeek planner quality contract 测试发现：
  - scene 1 返回文案“正宗川味，太上头！”。
  - 该文案中文字符数为 7。
  - 原 quality contract 将少于 8 个中文字符直接判为 `narration_too_short` error，导致整体 quality 失败。
- 本轮修正：
  - 空 narration 仍为 error。
  - 非中文 narration 仍为 error，错误码为 `non_chinese_narration`。
  - 少于 4 个中文字符的极短 narration 仍为 hard error，错误码为 `narration_too_short_hard`。
  - 4 到 7 个中文字符的中文短句降级为 warning，错误码为 `narration_too_short`。
  - `正宗川味，太上头！` 这类短促但可用于餐厅宣传片的中文文案可以通过 quality contract。
  - DeepSeek prompt 补充要求：每个 scene narration 应为自然中文短句，优先不少于 8 个中文字符，避免过短片段、mock、placeholder、TODO、待填写或 Markdown。
- 保留的硬性门禁：
  - 缺少 `narration`、`visual_instruction`、`selling_point`、`transition_hint` 仍为 error。
  - duplicate narration 仍为 error。
  - DeepSeek planner 中 mock / placeholder 文案仍为 error。
- 当前边界：
  - 本轮不调用 DeepSeek。
  - 本轮不调用任何外部 API。
  - 本轮不生成视频。
  - 未修改 WebUI、`app/` 或 `config.toml`。

## 第 2 阶段验证：DeepSeek Storyboard Quality Contract 真实复测通过

- 第 2 阶段 DeepSeek storyboard quality contract 真实复测已通过。
- 真实 DeepSeek storyboard 同时通过：
  - structure contract
  - quality contract
  - duration alignment
  - image order check
- 复测结果摘要：
  - `pipeline_report.ok=true`
  - `planner=deepseek`
  - `external_api_called=true`
  - `storyboard_contract_passed=true`
  - `storyboard_quality_passed=true`
  - `quality_errors=0`
  - `quality_warnings=3`
  - `target_duration_seconds=30`
  - `scene_durations=[4,4,3,4,4,3,4,4]`
  - `storyboard.total_duration_seconds=30`
  - `scene_count=image_count=8`
  - scene 顺序与图片顺序一致。
  - `narration` / `visual_instruction` / `selling_point` / `transition_hint` 均存在。
  - 未发现 mock 文案。
- 安全与边界：
  - 未发现 API Key 写入 `pipeline_report.json` 或 `storyboard.json`。
  - 未生成视频。
  - 未修改代码。
  - 当前阻塞问题：无。
  - 当前非阻塞问题：系统 `python3` 缺少项目依赖，实际使用 `.venv` Python 执行。

## 第 2 阶段补充：TTS Contract / Narration Plan 骨架

- 开始实现 TTS contract / narration plan 骨架。
- 本轮目标是在接入真实 TTS 前，先从 storyboard 生成本地 `narration_plan.json`。
- 新增能力：
  - 每个 storyboard scene 生成一条 narration line。
  - 记录 scene index、图片名、画面时长、旁白、中文字符数、估算朗读时长。
  - 根据中文字符数和 scene duration 做 TTS contract 校验。
  - `pipeline_report.json` 记录 TTS contract 结果。
  - CLI 输出 TTS contract 摘要。
- TTS contract 当前处理：
  - 空 narration、非中文 narration、无效 duration 为 error。
  - 估算朗读时长超过画面时长为 warning。
  - 明显超出画面时长的 narration 为 error。
- 当前边界：
  - 不生成音频。
  - 不调用 TTS。
  - 不调用 DeepSeek。
  - 不调用任何外部 API。
  - 不生成视频。
  - 未修改 WebUI。
  - 未修改 `app/`。
  - 未修改 `config.toml`。

## 第 2 阶段验证：DeepSeek Narration Plan / TTS Contract 真实复测通过

- 第 2 阶段 DeepSeek narration plan / TTS contract 真实复测已通过。
- 真实 DeepSeek storyboard 同时通过：
  - structure contract
  - quality contract
  - duration alignment
  - `narration_plan` 生成
  - TTS contract
- 复测结果摘要：
  - `pipeline_report.ok=true`
  - `planner=deepseek`
  - `external_api_called=true`
  - `storyboard_contract_passed=true`
  - `storyboard_quality_passed=true`
  - `tts_contract_passed=true`
  - `storyboard_quality_errors=0`
  - `tts_errors=0`
  - `target_duration_seconds=30`
  - `scene_durations=[4,4,3,4,4,3,4,4]`
  - `narration_line_count=8`
  - `estimated_total_tts_seconds=32.0`
  - `total_cjk_chars=128`
- 安全与边界：
  - 未生成音频。
  - 未生成视频。
  - 未修改代码。
  - 未发现 API Key 写入 report/storyboard/narration_plan。
  - 当前阻塞问题：无。
  - 当前非阻塞问题：估算朗读时长略超过目标，后续真实 TTS 阶段需要做音频时长校准。

## 第 2 阶段补充：Mock Image Understanding 骨架

- 开始实现 mock image understanding 骨架。
- 本轮目标是在进入 storyboard / TTS / 图生视频 / 视频合成前，为本地图片建立图片理解占位 contract。
- 新增能力：
  - 根据本地图片文件名生成 `image_understanding.json`。
  - 每张图片记录 mock 类型、质量分、封面分、视频分、风险分、是否允许进入视频和推荐动作。
  - `pipeline_report.json` 记录 `image_understanding_path`、`image_understanding_passed`、`allowed_image_count`、`rejected_image_count`、`image_category_counts`。
  - CLI 输出 image understanding 摘要。
- 当前规则：
  - `intro` / `interior` / `dish` / `dining` / `detail` / `extra` / `logo` / `other` 基于文件名识别。
  - 文件名包含二维码、电话、地址、菜单、价格、联系方式、微信等风险词时标记为 `invalid_*` 并拒绝进入视频。
  - 当前 rejected images 只产生 warning，不阻断 pipeline。
  - 没有图片时为 error，pipeline `ok=false`。
- 当前边界：
  - 不读取图片像素内容。
  - 不调用视觉模型或 OCR。
  - 不调用 DeepSeek。
  - 不调用任何外部 API。
  - 不调用 TTS。
  - 不生成音频或视频。
  - 未修改 WebUI、`app/`、`config.toml` 或 MoneyPrinterTurbo 视频生成核心。

## 第 3 阶段修正：图片理解 Provider 架构

- 用户确认：真实用户会用手机上传图片，文件名通常没有语义，不能依赖文件名识别图片类别。
- 本轮调整：
  - 图片内容识别被明确为正式主逻辑。
  - 文件名规则降级为 `filename_fallback`，只能作为开发兜底。
  - 默认 provider 改为 `mock`，只生成开发占位，不读取图片内容，也不使用文件名语义。
  - 新增 provider 概念：`mock` / `filename_fallback` / `vision`。
  - 未来真实视觉识别必须显式使用 `--image-understanding-provider vision --allow-external-api`。
  - 当前 `vision` provider 尚未实现，即使授权也不会调用外部 API。
- 当前边界：
  - 不调用 DeepSeek。
  - 不调用任何外部 API。
  - 不调用视觉模型或 OCR。
  - 不调用 TTS。
  - 不生成音频或视频。
  - 未修改 WebUI、`app/`、`config.toml` 或 MoneyPrinterTurbo 视频生成核心。

## 第 3 阶段补充：本地规则引擎骨架

- 开始实现本地 deterministic rule engine contract。
- 规则引擎位置：
  - `image_understanding.json` 之后。
  - `storyboard.json` 之前。
- 新增输出：
  - `rule_engine_report.json`
- 当前规则引擎：
  - `engine=local_static`
  - `external_api_called=false`
  - 只消费 `image_understanding` 的结构化结果。
  - 不重新读取文件名。
  - 不读取图片像素内容。
  - 不调用视觉模型、OCR、DeepSeek、TTS 或任何外部 API。
- 当前输出字段：
  - `summary`
  - `findings`
  - `asset_groups`
  - `storyboard_hints`
  - `blocking`
- 当前 provider 行为：
  - `mock` 输出 `NO_CONTENT_BASED_UNDERSTANDING` warning。
  - `filename_fallback` 输出 `FILENAME_FALLBACK_USED` warning。
  - 两者当前都不阻断 pipeline，但会标记需要人工复核。
- `pipeline_report.json` 新增：
  - `rule_engine_report_path`
  - `rule_engine_external_api_called`
  - `rule_engine_findings_count`
  - `rule_engine_blocking`
  - `rule_engine_version`
- 当前边界：
  - 不生成音频。
  - 不生成视频。
  - 不调用 DeepSeek。
  - 不调用任何外部 API。
  - 未修改 WebUI、`app/`、`config.toml` 或 MoneyPrinterTurbo 视频生成核心。

## 第 3 阶段收口验收：Contract Freeze

- 第 3 阶段进入 contract freeze / acceptance。
- 新增 `restaurant_docs/STAGE_3_ACCEPTANCE.md`。
- 冻结第 4 阶段可依赖的输入边界：
  - `image_understanding.json`
  - `rule_engine_report.json`
  - `storyboard.json`
  - `narration_plan.json`
  - `pipeline_report.json`
- 补齐 `image_understanding` 顶层 `analysis_source` 与 `external_api_called` 字段。
- 补齐 `pipeline_report.json` 中 `image_understanding_analysis_source` 字段。
- 当前确认：
  - `mock` 是默认 provider。
  - `filename_fallback` 只能显式启用，且不是正式图片内容理解。
  - `vision` 当前仍为受控未实现 stub。
  - `rule_engine` 为 `local_static`，只消费 `image_understanding`。
  - `rule_engine` 不重新根据文件名分类，不读取图片像素，不调用外部 API。
  - 当前未进入第 4 阶段，未实现封面生成。
- 当前边界：
  - 不调用 DeepSeek。
  - 不调用视觉模型。
  - 不调用 TTS。
  - 不生成音频或视频。
  - 未修改 WebUI、`app/`、`config.toml`、`storage/` 或 `resource/`。

## 第 4 阶段启动：封面方案 Contract 骨架

- 第 4 阶段“封面生成模块”已开始。
- 本轮只实现标题候选、用户选择标题和 `cover_plan.json` contract 骨架。
- 新增本地静态 cover planner：
  - `planner=local_static`
  - `external_api_called=false`
  - `render_status=not_rendered`
  - `cover_image_path=null`
- 新增 `restaurant_engine/cover_planner.py`。
- 新增 `restaurant_docs/COVER_PLAN_SPEC.md`。
- pipeline 顺序调整为：
  - load project
  - validator
  - scan images
  - image_understanding
  - rule_engine
  - cover_plan
  - storyboard
  - narration_plan
  - pipeline_report
- 支持 `project.json` 可选字段：
  - `theme_text`
  - `selected_cover_title_id`
  - `selected_cover_title`
  - `selected_cover_image_id`
- 当前标题生成：
  - 本地静态生成 3 个标题候选。
  - 用户选择标题作为 `selected_title`。
  - `cover_copy.title` 必须等于 `selected_title.text`。
- 当前封面图片选择：
  - 优先使用用户指定图片。
  - 否则使用 rule engine 的 opening / hero / dish / interior / fallback 候选。
  - 最后 fallback 到上传图片第一张。
- `pipeline_report.json` 新增 cover 摘要字段：
  - `cover_plan_path`
  - `cover_planner`
  - `cover_external_api_called`
  - `cover_render_status`
  - `cover_image_path`
  - `cover_selected_image_id`
  - `cover_selected_title`
  - `cover_title_candidates_count`
  - `cover_title_user_selected`
  - `cover_requires_human_review`
  - `cover_blocking`
- 当前边界：
  - 本轮暂不 commit，等待用户确认后再提交。
  - 不生成真实封面图片。
  - 不输出 PNG / JPG / JPEG / WebP 封面文件。
  - 不调用 DeepSeek。
  - 不调用任何外部 API。
  - 不读取 API Key。
  - 不读取图片像素。
  - 不重新根据文件名分类。
  - 不调用 TTS。
  - 不生成音频或视频。
  - 未修改 WebUI、`app/`、`config.toml` 或 MoneyPrinterTurbo 视频生成核心。

## 第 4 阶段继续：本地封面渲染 Renderer 骨架

- 第 4 阶段第 2 个任务开始：本地封面图渲染 renderer 骨架。
- 新增 `restaurant_engine/cover_renderer.py`。
- 新增 `restaurant_docs/COVER_RENDER_SPEC.md`。
- renderer 当前为 `local_pillow`。
- 输入来自 `cover_plan.json`：
  - `selected_title.text`
  - `cover_copy.title`
  - `selected_assets.primary_image_path`
- 渲染输出：
  - `cover_image.png`
  - `cover_render_report.json`
- 输出规格：
  - PNG
  - 1080 x 1920
  - 9:16
- pipeline 顺序调整为：
  - load project
  - validator
  - scan images
  - image_understanding
  - rule_engine
  - cover_plan
  - cover_renderer
  - storyboard
  - narration_plan
  - pipeline_report
- `pipeline_report.json` 新增封面渲染字段：
  - `cover_render_report_path`
  - `cover_renderer`
  - `cover_render_external_api_called`
  - `cover_render_status`
  - `cover_rendered_image_path`
  - `cover_render_output_width`
  - `cover_render_output_height`
  - `cover_render_source_image_id`
  - `cover_render_title_text`
  - `cover_render_blocking`
- 当前采用保守 contract：
  - `cover_plan.json` 保持原始方案，不回写为 rendered。
  - 渲染结果写入 `cover_render_report.json` 与 `pipeline_report.json`。
- 当前边界：
  - 本轮暂不 commit，等待用户确认后再提交。
  - 只使用当前环境已存在的 Pillow / PIL。
  - 不安装依赖。
  - 不复制或提交字体文件。
  - 不调用 DeepSeek。
  - 不调用任何外部 API。
  - 不调用视觉模型或 AI 图片生成。
  - 不读取 API Key。
  - 不调用 TTS。
  - 不生成音频或视频。
  - 未修改 WebUI、`app/`、`config.toml`、`storage/` 或 `resource/`。

## 第 4 阶段收口：封面生成 Contract Freeze / Acceptance

- 第 4 阶段封面生成模块进入 contract freeze / acceptance。
- 新增验收文档：
  - `restaurant_docs/STAGE_4_ACCEPTANCE.md`
- 已冻结第 5 阶段可依赖的 cover contract：
  - `cover_plan.json`
  - `cover_render_report.json`
  - `pipeline_report.json` 中的 cover plan / cover render 字段
- 第 5 阶段可依赖：
  - `cover_plan.selected_title.text`
  - `cover_plan.cover_copy.title`
  - `cover_plan.title_candidates`
  - `cover_plan.selected_assets.primary_image_id`
  - `cover_plan.selected_assets.primary_image_path`
  - `cover_render_report.cover_image_path`
  - `cover_render_report.title_text`
  - `cover_render_report.source_image_id`
  - `cover_render_report.output_width`
  - `cover_render_report.output_height`
  - `pipeline_report.cover_rendered_image_path`
  - `pipeline_report.cover_render_title_text`
- 第 5 阶段不得假设：
  - 已经有真实图片内容理解。
  - `detected_type` 一定准确。
  - `filename_fallback` 是正式分类能力。
  - `cover_image.png` 是 AI 生成图片。
  - 可以调用外部 API、DeepSeek、TTS 或生成音频/视频。
  - WebUI 是最终产品。
- 本轮验收边界：
  - 不进入第 5 阶段。
  - 不调用 DeepSeek。
  - 不调用任何外部 API。
  - 不调用 TTS。
  - 不生成音频或视频。
  - 不修改 WebUI、`app/`、`config.toml`、`storage/` 或 `resource/`。
  - 本轮暂不 commit，等待后续提交前复核。

## 第 4 阶段：WebUI 临时封面验证入口

- 在 MoneyPrinterTurbo Streamlit WebUI 中新增餐饮封面生成临时验证入口。
- 该入口只用于第 4 阶段本地验证，不是最终正式 Web 产品，也不是后续 `restaurant-video-ai` 项目。
- WebUI 支持：
  - 输入 `theme_text`。
  - 本地生成 3 个标题候选。
  - 用户选择 `selected_cover_title_id`。
  - 上传 1 张或多张餐厅图片。
  - 用户选择封面图片或选择自动。
  - 调用 `restaurant_engine` 本地 pipeline 生成封面。
  - 预览 `cover_image.png`。
  - 展示 cover plan / render / pipeline 摘要。
- 当前复用：
  - `restaurant_engine.cover_planner.build_title_candidates`
  - `restaurant_engine.pipeline.run_pipeline`
  - `cover_plan.json`
  - `cover_render_report.json`
  - `cover_image.png`
  - `pipeline_report.json`
- 新增临时 project 模式：
  - `pipeline_mode=cover_prototype`
  - 仅用于 WebUI 封面验证。
  - 允许封面验证在上传 1 张图片时运行。
  - 不改变默认视频主流程的图片数量和类别门禁。
- 上传图片和输出产物写入仓库外：
  - `/private/tmp/mpt-restaurant-webui/`
- 当前边界：
  - 不进入第 5 阶段。
  - 不调用 DeepSeek。
  - 不调用任何外部 API。
  - 不调用 LLM。
  - 不读取 API Key。
  - 不调用视觉模型。
  - 不使用 AI 图片生成。
  - 不调用 TTS。
  - 不生成音频或视频。
  - 不修改 `app/`、`config.toml`、`storage/` 或 `resource/`。
  - 本轮暂不 commit，等待浏览器确认和提交前复核。

## 第 4 阶段：WebUI 标题/文案一体化调整

- 调整 WebUI 临时封面验证入口的交互。
- 主按钮改为：
  - `生成视频标题/视频文案`
- 用户输入视频主题后，点击该按钮会同时生成：
  - 3 个视频标题候选
  - 本地 mock 视频文案
- 标题候选显示在按钮下方，并供用户选择。
- 视频文案显示在标题候选区域下方。
- 独立 `生成标题候选` 主流程动作已合并，不再要求用户单独点击。
- 视频文案当前复用 `restaurant_engine.storyboard_planner.build_mock_storyboard` 的本地 mock 能力。
- 封面生成仍使用：
  - `selected_cover_title_id`
  - `cover_plan.json`
  - `cover_render_report.json`
  - `cover_image.png`
  - `local_pillow`
- 当前边界：
  - 不进入第 5 阶段。
  - 不调用 DeepSeek。
  - 不调用任何外部 API。
  - 不调用 LLM。
  - 不使用 AI 图片生成。
  - 不调用 TTS。
  - 不生成音频或视频。
  - 不修改 `app/`、`config.toml`、`storage/` 或 `resource/`。
  - 本轮暂不 commit。

## 第 4 阶段：文案设置中的标题/文案一体化修正

- 根据最新产品反馈，标题候选生成不应作为独立入口或独立页面出现。
- 当前已将一体化动作并入现有 WebUI 左侧 `文案设置` 区域。
- 原文案设置按钮显示调整为：
  - `生成视频标题/视频文案`
- 用户在 `视频主题` 输入主题后，点击该按钮会：
  - 继续执行原有视频文案生成逻辑。
  - 本地生成 3 个封面标题候选。
  - 默认选择 `title_1`。
  - 将标题候选显示在按钮下方，供用户切换。
- 封面生成验证区不再提供独立主题输入或独立标题/文案生成按钮。
- 封面生成继续读取：
  - `restaurant_cover_selected_title_id`
  - 用户上传图片
  - 本地 `restaurant_engine` cover pipeline
- 当前仍是本地 prototype：
  - 不进入第 5 阶段。
  - 不调用 DeepSeek。
  - 不调用任何外部 API。
  - 不调用 AI 图片生成。
  - 不调用 TTS。
  - 不生成音频或视频。
  - 不修改 `config.toml`、`storage/` 或 `resource/`。
  - 本轮暂不 commit，等待浏览器确认和提交前复核。

## 第 4 阶段：本地标题候选质量修正

- 针对 WebUI 封面标题候选质量偏弱的问题，优化本地 `local_static` 标题模板。
- 原弱模板问题：
  - `四川火锅值得一试`
  - `四川火锅聚餐首选`
  - `发现这家四川火锅`
- 新策略：
  - 不再使用简单 `主题 + 后缀` 拼接。
  - 按本地规则识别火锅、川菜、烤鱼、小龙虾、咖啡甜品、烧烤等常见餐饮场景。
  - 固定输出 3 个不同角度标题：
    - 味道钩子
    - 场景钩子
    - 氛围/发现感钩子
  - 标题保持短句，更适合作为短视频封面主标题。
- 标题生成仍为 deterministic 本地逻辑：
  - `source=local_static`
  - 不调用 DeepSeek。
  - 不调用 LLM。
  - 不调用任何外部 API。
  - 不使用 AI 图片生成。
- WebUI 继续复用 `restaurant_engine.cover_planner.build_title_candidates`，pipeline 和 WebUI 标题候选保持一致。
- 当前仍不进入第 5 阶段，不生成音频或视频，本轮暂不 commit。

## 第 4 阶段：WebUI 视频设置区生成封面入口

- 将 `生成封面` 按钮移动到中间列 `视频设置` 区域。
- 按钮位于 `当前本地图片数量：X 张` 下方。
- 封面生成复用视频设置中的本地上传图片，不再提供独立封面图片上传入口。
- 保留文案设置中的 `生成视频标题/视频文案` 和标题候选选择。
- 点击 `生成封面` 时：
  - 未上传图片：显示受控提示，不调用 pipeline。
  - 未生成并选择标题：显示受控提示，不调用 pipeline。
  - 图片和标题均满足时：调用本地 `restaurant_engine` cover pipeline，生成 `cover_image.png` 和摘要。
- 继续固定使用本地 mock / local renderer：
  - `planner=mock`
  - `image_understanding_provider=mock`
  - `allow_external_api=false`
- 本轮只调整 WebUI 展示与本地封面入口，不调用 DeepSeek、不调用外部 API、不生成音频或视频、不修改 MoneyPrinterTurbo 视频生成核心。

## 第 4 阶段：WebUI 标题/文案按钮本地安全路径

- 修正文案设置区 `生成视频标题/视频文案` 按钮的餐饮封面 prototype 点击逻辑。
- 点击后改为本地安全路径：
  - 读取当前视频主题。
  - 调用 `restaurant_engine.cover_planner.build_title_candidates` 生成 3 个标题候选。
  - 标题候选固定为 `title_1` / `title_2` / `title_3`，`source=local_static`。
  - 默认选中 `title_1`，用户仍可切换 `title_2` / `title_3`。
  - 本地生成 prototype 视频文案，并写入现有 `视频文案` 输入框。
- 餐饮封面 prototype 下不再进入原 LLM 文案生成路径，也不调用关键词 API。
- prototype 视频文案只用于第 4 阶段 WebUI 临时验证入口，不是第 5 阶段正式文案系统。
- 封面生成链路保持不变，仍读取当前 `restaurant_cover_selected_title_id`。
- 安全边界：
  - 不调用 DeepSeek。
  - 不调用任何外部 API。
  - 不调用 LLM。
  - 不读取 API Key。
  - 不生成音频或视频。
  - 不修改 `app/`、`config.toml`、`storage/` 或 `resource/`。
  - 本轮暂不 commit。

## 第 4 阶段：RunningHub 批量封面 WebUI Prototype

- 调整 WebUI 封面生成交互：
  - `文案设置` 主按钮改为 `生成视频文案`，只生成本地 prototype 视频文案。
  - 不再在前台展示标题候选列表，不再让用户选择标题。
  - 点击 `生成封面` / `重新生成封面` 时，后台本地生成 3 条 `local_static` 标题。
  - 上传图片少于 3 张时，封面按钮 disabled，并提示至少上传 3 张图片。
  - 上传图片达到 3 张后，WebUI 随机选择 3 张用户上传图片。
  - 系统将 3 张图片和 3 条标题一一配对，提交 RunningHub batch。
  - 成功后展示 3 张封面图，用户可选择其中 1 张，选中项有高亮。
- 新增 `restaurant_engine/runninghub_cover.py`：
  - 读取 RunningHub 环境变量配置。
  - 上传图片、提交任务、轮询结果、下载图片。
  - 输出 `cover_batch_report.json`。
  - 缺配置时受控失败，不 fallback 到本地伪结果。
- 当前边界：
  - 不调用 DeepSeek。
  - 不调用 LLM。
  - 不调用非 RunningHub 外部 API。
  - 不生成音频或视频。
  - 不修改 `app/`、`config.toml`、`storage/` 或 `resource/`。
  - 本轮暂不 commit，等待复核。

## 第 4 阶段：RunningHub Workflow API JSON 校准

- 已只读检查用户 Downloads 中的 RunningHub workflow JSON：
  - `/Users/feei/Downloads/视频封面设计-全能图片G2图像编辑（RH版）_api.json`
  - `/Users/feei/Downloads/视频封面设计-全能图片G2图像编辑（RH版）.json`
- 下载的 workflow JSON 只作为本机参考，不复制进仓库，不提交 Git。
- 参考 workflow：
  - URL：`https://www.runninghub.cn/workflow/2064397787445424129`
  - workflow id：`2064397787445424129`
- 从 `_api.json` 提取到的非敏感节点映射：
  - 图片输入：`13.image`
  - 标题/提示词输入：`3.prompt`
  - 输出保存：`4.images`
- `restaurant_engine/runninghub_cover.py` 已按该 workflow 做最小校准：
  - 标题字段默认改为 `prompt`。
  - 支持 `RUNNINGHUB_COVER_IMAGE_NODE_FIELD`。
  - 支持 `RUNNINGHUB_COVER_TITLE_NODE_FIELD`。
  - 支持 `RUNNINGHUB_COVER_OUTPUT_NODE_ID` / `RUNNINGHUB_COVER_OUTPUT_NODE_FIELD`。
  - 保留 `RUNNINGHUB_COVER_NODE_INFO_JSON` 作为复杂 node mapping 入口。
- 当前未执行真实 RunningHub 任务，等待用户后续明确授权。
- 未调用 DeepSeek、LLM、TTS、音频或视频生成。
- 未修改 `app/`、`config.toml`、`storage/` 或 `resource/`。
- 本轮暂不 commit。

## 第 4 阶段：RunningHub 封面提示词与视频比例参数接入

- 继续完善 RunningHub 封面生成质量，不进入第 5 阶段。
- 标题仍为本地 `local_static`，不调用 DeepSeek、LLM 或外部文案 API。
- 本地标题规则升级为更适合短视频封面的 3 条高吸引力标题：
  - 建议 6–16 个中文字符。
  - 禁用 `值得一试`、`聚餐首选`、`发现这家`、`不容错过`、`强烈推荐`、`必吃`、`宝藏`、`绝了` 等弱模板。
  - 禁用 `全城第一`、`天花板`、`史上最强`、`全网爆火`、`100% 好吃`、`不吃后悔` 等夸张承诺。
  - 重新生成封面时会按 batch index 刷新标题批次。
- RunningHub prompt 节点改为接收完整 `cover_prompt`：
  - 包含主题、标题文字、艺术感/顶级设计感/爆款封面等风格要求。
  - 包含 `文字：“...”`。
  - 包含当前视频比例。
- WebUI 复用现有 `视频比例` 字段，支持 `9:16` 和 `16:9`，不新增重复控件。
- RunningHub provider 新增可选比例节点配置：
  - `RUNNINGHUB_COVER_RATIO_NODE_ID`
  - `RUNNINGHUB_COVER_RATIO_NODE_FIELD`
  - `RUNNINGHUB_COVER_RATIO_16_9_VALUE`
  - `RUNNINGHUB_COVER_RATIO_9_16_VALUE`
- 未配置比例节点时，比例仍写入 prompt，并在 report 记录 `RATIO_NODE_NOT_CONFIGURED_PROMPT_ONLY`。
- `cover_batch_report.json` 新增记录：
  - 顶层 `aspect_ratio`、`prompt_style_version`、`title_quality_version`。
  - variant 级 `title_quality_passed`、`title_quality_warnings`、`cover_prompt`、`prompt_source`、`aspect_ratio`。
- WebUI 仍不展示标题候选列表或标题选择 UI，只展示封面编号、预览、选中状态、比例、渲染状态和 warning。
- 本轮不执行真实 RunningHub smoke，不调用 DeepSeek、LLM、TTS，不生成音频或视频。
