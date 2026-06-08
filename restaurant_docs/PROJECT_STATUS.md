# 项目状态

## 项目基本信息

- 项目名称：餐饮 AI 宣传视频生成系统
- 当前仓库：/Users/feei/AI/MoneyPrinterTurbo
- 当前分支：feature/restaurant-video-prototype
- 当前阶段：第 2 阶段：餐厅专用镜头计划 / 参数预检器（preflight 目标时长计算实现中）
- 当前下一步：让 preflight 使用 target_duration_seconds 动态计算推荐 clip duration、图片总覆盖时长和旁白字数上限；暂不修改 checklist，不改 MoneyPrinterTurbo 原业务代码。

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
