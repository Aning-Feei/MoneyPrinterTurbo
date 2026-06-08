# 任务记录

## 已完成任务

- 修复 Codex service_tier 配置
- 纠正 Codex 错误工作目录问题
- 正确打开 MoneyPrinterTurbo 项目
- 创建开发分支
- 创建 restaurant_docs 和 restaurant_engine
- 准备样本图片并补齐 6 张
- 创建样本 project.json
- 创建 Codex 执行控制规范
- 创建 restaurant_engine 最小只读校验器

## 第 0 阶段 0.9 - 创建 restaurant_engine 最小只读校验器

- 新增或更新文件：
  - restaurant_engine/__init__.py
  - restaurant_engine/models.py
  - restaurant_engine/validator.py
  - restaurant_engine/validate_project.py
  - restaurant_docs/VALIDATOR_SPEC.md
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- 校验范围：
  - 读取仓库外 project.json
  - 检查必填字段
  - 检查 aspect_ratio
  - 检查 image_dir 是否存在
  - 扫描 jpg/jpeg/png 图片文件名
  - 检查图片数量 6 到 12 张
  - 检查命名类别占位规则
  - 检查禁止内容文件名关键词
- 测试命令：
  - export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
  - uv run python -m py_compile restaurant_engine/*.py
  - uv run python -m restaurant_engine.validate_project --project /Users/feei/AI/restaurant-video-ai-samples/sichuan_001/project.json
  - git status --short -- restaurant_engine restaurant_docs/VALIDATOR_SPEC.md restaurant_docs/PROJECT_STATUS.md restaurant_docs/TASK_LOG.md config.toml pyproject.toml uv.lock .gitignore
- 测试结果：
  - py_compile 通过
  - validate_project 通过
  - validation_report.json 已生成
  - validation_report.json passed 为 true
- 下一步：
  - 第 1 阶段：MoneyPrinterTurbo 基础生成链路验证

## 第 1 阶段 - MoneyPrinterTurbo 基础生成链路只读检查

- 本次目标：
  - 只读检查 MoneyPrinterTurbo 当前基础生成链路相关入口
  - 确认后续如何用现有能力做一次餐饮视频基础生成测试
- 实际读取：
  - webui.sh
  - webui/Main.py
  - app/services/task.py
  - app/services/video.py
  - app/services/voice.py
  - app/models/schema.py
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- 检查结论：
  - WebUI 通过 webui.sh 启动 Streamlit，并运行 webui/Main.py
  - 本地素材入口位于 webui/Main.py 的 video_source 选择和 Local file 上传逻辑
  - 基础视频参数结构位于 app/models/schema.py
  - voice_name 来源位于 webui/Main.py 的语音选择逻辑和 app/services/voice.py 的解析逻辑
  - 字幕开关、字幕位置、BGM 类型、BGM 文件和 BGM 音量位于 webui/Main.py 与 app/models/schema.py
  - 本地素材预处理入口位于 app/services/task.py 调用 app/services/video.py 的 preprocess_video
  - 视频合成入口位于 app/services/task.py 调用 app/services/video.py 的 combine_videos
- 禁止行为确认：
  - 未修改 MoneyPrinterTurbo 原有业务代码
  - 未生成视频
  - 未调用 DeepSeek
  - 未调用 TTS
  - 未调用 AI 图生视频
  - 未安装依赖
  - 未调用外部 API
- 下一步：
  - 进行一次不改代码的基础生成测试：启动 WebUI，选择 Local file，上传仓库外样本图片，使用现有 voice_name、字幕和 BGM 参数完成一次最小生成链路验证。

## 第 1 阶段 - WebUI 启动和浏览器冒烟测试

- WebUI 启动命令：
  - sh ./webui.sh
- WebUI 地址：
  - http://127.0.0.1:8501
- WebUI 启动结果：
  - 启动成功
  - 进程仍在运行
- 浏览器测试结果：
  - WebUI 打开成功
  - 页面无红色报错
  - 主要页面/Tab 可用
  - 已点击生成按钮
  - 用户反馈已调用外部 API
  - 用户反馈已生成文件
  - 终端暂无新增错误日志
- 生成产物：
  - 是否生成文件：用户反馈已生成文件
  - 生成文件路径：待补充，用户未提供具体路径
  - 生成文件名：待补充，用户未提供具体名称
- 外部服务：
  - 是否调用外部 API：是，用户反馈已调用
  - 外部 API provider：待补充，用户未提供具体 provider
- 错误情况：
  - 页面红色报错：未发现
  - 终端新增错误日志：暂无
  - TTS 错误：未发现明确错误
  - 字幕错误：未发现明确错误
  - BGM 错误：未发现明确错误
  - ffmpeg 错误：未发现明确错误
- 限制说明：
  - 本次未修改 MoneyPrinterTurbo 原有业务代码
  - 本次未修改配置文件
  - 本次未安装依赖
  - 本次未由 Codex 主动调用外部 API
- 下一步：
  - 补充生成文件具体路径和文件名
  - 补充实际外部 API provider
  - 根据产物确认是否进入第 2 阶段 restaurant_engine Pipeline 骨架

## 第 1 阶段 - WebUI 生成产物只读定位

- 本次目标：
  - 只读搜索 WebUI 点击生成后的产物路径和文件类型
  - 不修改业务代码，不提交任何 storage/ 产物
- 任务目录：
  - storage/tasks/6b4c0e38-8df8-4991-87cd-ad495ab090df
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

## 第 1 阶段 - final-1.mp4 人工播放检查

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

## 第 1 阶段 - 图片顺序不合理只读根因定位

- 本次目标：
  - 只读定位 final-1.mp4 中图片顺序不合理的原因
  - 不修改业务代码，不实施修复
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

## 第 1 阶段 - 第二次 WebUI Sequential 复测和循环原因定位

- 本次目标：
  - 记录第二次 WebUI 无代码复测结果
  - 定位 6 张图片播放两遍的原因
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

## 第 1 阶段 - 第三次 WebUI 参数基线复测

- 本次目标：
  - 定位第三次复测最新 task
  - 记录 6 秒时长参数下的 WebUI 基础生成结果
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

## 第 2 阶段 - 最小版餐厅视频预检器

- 本次目标：
  - 实现纯本地、只读、规则型预检器
  - 输入 project.json + 图片目录 + 旁白文本
  - 输出 preflight_report.json
- 新增文件：
  - restaurant_engine/preflight.py
  - restaurant_engine/preflight_project.py
  - restaurant_docs/PREFLIGHT_SPEC.md
- 修改文件：
  - restaurant_engine/models.py
  - restaurant_engine/__init__.py
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- 预检器能力：
  - 生成餐厅镜头顺序计划
  - 估算旁白时长
  - 推荐 video_clip_duration
  - 判断图片循环风险
  - 推荐 WebUI 参数
  - 输出 warnings/errors
- 运行约束：
  - 不调用外部 API
  - 不调用 DeepSeek
  - 不调用 TTS
  - 不读取图片内容做视觉识别
  - 不生成视频
  - 不修改 MoneyPrinterTurbo 原有业务代码

## 第 2 阶段 - 预检器负向测试

- 本次目标：
  - 验证预检器在图片数量少、旁白较长时是否能识别循环风险并给出合理参数建议
- 临时测试目录：
  - /tmp/mpt-preflight-negative/
- 临时 project：
  - /tmp/mpt-preflight-negative/project.json
- 临时报告：
  - /tmp/mpt-preflight-negative/preflight_report.json
- 输入特征：
  - 只有 3 张图片：
    1. 01_intro.jpg
    2. 02_interior.jpg
    3. 03_dish_1.jpg
  - 旁白较长
- 测试命令：
  - python3 -m restaurant_engine.preflight_project /tmp/mpt-preflight-negative/project.json
- 测试结果：
  - 预检器运行成功
  - 命令退出码为 1
  - 退出码为 1 的原因是报告 ok: false，属于负向测试预期，不是程序崩溃
  - 仓库内未出现 preflight_report.json
  - git status --short 保持为空
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
  - CLI 可以更明确地区分“程序执行失败”和“预检完成但 ok=false”
  - 例如在控制台输出 preflight completed with validation errors
  - 该改进不阻塞当前阶段

## 第 2 阶段 - 预检器 CLI 提示改进

- 本次目标：
  - 当预检完成但 ok=false 时，明确提示“预检已完成，但存在校验错误”
  - 避免用户把负向测试的退出码 1 误判为 Python 程序崩溃
- 修改范围：
  - restaurant_engine/preflight_project.py
  - restaurant_docs/PREFLIGHT_SPEC.md
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- 行为调整：
  - ok=true 时返回退出码 0，并打印 preflight completed successfully
  - ok=false 时返回退出码 1，并打印 preflight completed with validation errors: 预检已完成，但存在校验错误
  - 程序异常时返回退出码 2，并打印 preflight failed: ...
- 未修改内容：
  - 未修改 shot 排序逻辑
  - 未修改旁白估算逻辑
  - 未修改 clip duration 推荐逻辑
  - 未修改 will_loop 判断逻辑
  - 未修改 MoneyPrinterTurbo 原有业务代码

## 当前阶段收口总结

- 第 1 阶段完成：
  - WebUI 成功启动
  - WebUI 基础餐厅图文视频生成链路通过
  - 可用样片 task：2dceacbf-bf55-494a-8004-a3f0eacfb067
  - 可用样片：storage/tasks/2dceacbf-bf55-494a-8004-a3f0eacfb067/final-1.mp4
  - 推荐 WebUI 参数基线：
    - 完整 6 张图
    - Sequential/顺序拼接
    - video_clip_duration = 6
    - 确保 图片数 * 每张图片时长 >= 旁白时长
- 第 2 阶段当前完成：
  - restaurant_engine 已有只读 validator
  - 已新增 preflight planner
  - 可生成 preflight_report.json
  - 正向样本通过
  - 负向样本可识别图片不足、角色缺失和循环风险
  - CLI 已明确区分 preflight completed successfully 和 preflight completed with validation errors: 预检已完成，但存在校验错误
- 当前代码边界：
  - 未修改 MoneyPrinterTurbo 原业务代码
  - 未接入 WebUI
  - 未调用外部 API
  - 不生成视频，只做生成前预检
  - 生成产物和 preflight_report.json 不进入 Git
- 当前可用命令：
  - python3 -m restaurant_engine.validate_project /Users/feei/AI/restaurant-video-ai-samples/sichuan_001/project.json
  - python3 -m restaurant_engine.preflight_project /Users/feei/AI/restaurant-video-ai-samples/sichuan_001/project.json
- 下一步建议：
  - 增加更清晰的 WebUI 参数填表指南
  - 或把 preflight_report.json 转成“人工操作清单”
  - 或继续做结构化镜头计划，但仍暂不改 MoneyPrinterTurbo 原业务代码
  - 出差/换电脑前建议 push 当前分支到远程仓库
