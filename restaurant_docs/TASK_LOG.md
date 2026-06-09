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

## 第 2 阶段 - WebUI 操作清单最小实现

- 本次目标：
  - 把 preflight_report.json 转成人工 WebUI 填表指南
  - 输出 webui_checklist.md
- 新增文件：
  - restaurant_engine/webui_checklist.py
  - restaurant_docs/WEBUI_CHECKLIST_SPEC.md
- 修改文件：
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- 工具能力：
  - 读取 preflight_report.json
  - 生成项目状态摘要
  - 生成图片上传顺序
  - 生成 WebUI 参数建议
  - 生成旁白/时长检查
  - 保留 warnings/errors
  - 生成前确认清单
- 运行约束：
  - 不调用外部 API
  - 不生成视频
  - 不读取 storage/ 产物
  - 不修改 MoneyPrinterTurbo 原有业务代码

## 餐厅视频半自动流程收口

- 当前半自动流程已形成：
  - project.json
  - python3 -m restaurant_engine.validate_project <project.json>
  - python3 -m restaurant_engine.preflight_project <project.json>
  - python3 -m restaurant_engine.webui_checklist <preflight_report.json>
  - 人工按 webui_checklist.md 填 WebUI
  - 生成视频
- 当前已有工具：
  - restaurant_engine.validate_project：只读校验 project.json 和图片素材规范
  - restaurant_engine.preflight_project：生成 preflight_report.json，输出镜头顺序、旁白时长估算、clip duration 推荐、循环风险、WebUI 参数建议
  - restaurant_engine.webui_checklist：读取 preflight_report.json，生成 webui_checklist.md，正向样本提示可以生成，负向样本提示不建议生成并列出风险
- 当前已验证：
  - 第 1 阶段：WebUI 餐厅图文视频样片跑通
  - preflight 正向样本通过
  - preflight 负向样本能发现图片不足、角色缺失、循环风险
  - checklist 正向样本能生成 WebUI 填表清单
  - checklist 负向样本能明确提示不建议生成
- 当前边界：
  - 未修改 MoneyPrinterTurbo 原业务代码
  - 未接入 WebUI 自动填表
  - 未调用外部 API
  - 未生成视频
  - 只做生成前校验、预检和人工操作清单
  - preflight_report.json 和 webui_checklist.md 生成在样本目录或临时目录，不进入 Git
  - storage/ 和生成产物不进入 Git
- 当前建议下一步：
  - 可选方向 A：继续增强 webui_checklist.md，加入更具体的 WebUI 页面字段映射
  - 可选方向 B：增加结构化镜头计划字段，例如每个 shot 的标题、旁白片段、画面用途
  - 可选方向 C：准备 push 当前分支到 GitHub，方便换电脑继续
  - 不建议立即修改 MoneyPrinterTurbo 原业务代码

## 第 2 阶段 - WebUI 操作清单字段映射增强

- 本次目标：
  - 让 webui_checklist.md 更贴近真实 WebUI 表单
  - 写入真实 WebUI 字段名称、后端字段和值
  - 写入人工填表步骤和生成前确认清单
- 修改文件：
  - restaurant_engine/webui_checklist.py
  - restaurant_docs/WEBUI_CHECKLIST_SPEC.md
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- 新增输出内容：
  - WebUI 页面操作步骤
  - 真实字段映射表
  - 风险结论
  - 不要写死的字段提示
  - 更完整的生成前确认清单
- 保持不变：
  - 继续只读取 preflight_report.json
  - 继续在同目录生成 webui_checklist.md
  - 不调用外部 API
  - 不生成视频
  - 不读取 storage/ 产物
  - 不修改 MoneyPrinterTurbo 原有业务代码
  - 不修改 restaurant_engine/preflight.py

## 第 2 阶段 - 目标视频时长规则规格设计

- 本次目标：
  - 只更新规格文档
  - 引入目标视频时长、动态 video_clip_duration、图片数量范围和旁白字数安全上限
  - 暂不修改 restaurant_engine 代码
  - 暂不修改 MoneyPrinterTurbo 原业务代码
- 背景问题：
  - hotpot_001 第二样本 validate/preflight/checklist 均通过
  - checklist 推荐 video_clip_duration = 5
  - 用户按 checklist 在 WebUI 中使用 Local file、Sequential/顺序、6 张图片生成视频
  - WebUI 实际 audio.mp3 约 39.72 秒
  - 6 张图 * 5 秒 = 30 秒
  - 实际音频长于图片总时长，导致图片重复播放
- 规格结论：
  - 新样本应新增 `target_duration_seconds`
  - 合法值为 30、40、50、60
  - 旧样本缺少该字段时当前阶段可兼容，但应提示 warning
  - 新样本必须显式填写
- 动态 clip duration 规则：
  - raw_clip_duration = ceil(target_duration_seconds / image_count)
  - recommended_clip_duration = clamp(raw_clip_duration, 3, 6)
  - total_image_duration = image_count * recommended_clip_duration
  - will_loop = total_image_duration < max(target_duration_seconds, estimated_narration_seconds)
- 图片数量范围：
  - 30 秒：6-10 张
  - 40 秒：7-12 张
  - 50 秒：9-16 张
  - 60 秒：10-20 张
  - 如果继续保留当前最大 12 张限制，50 秒和 60 秒仍可生成，但需要更谨慎控制文案和节奏
- 旁白字数安全上限：
  - narration_safe_seconds = target_duration_seconds - 3
  - narration_max_cjk_chars = floor(narration_safe_seconds * 4.0)
  - 30 秒：约 108 中文字符
  - 40 秒：约 148 中文字符
  - 50 秒：约 188 中文字符
  - 60 秒：约 228 中文字符
- checklist 后续要求：
  - 展示目标视频时长
  - 展示当前图片数量和合理范围
  - 展示推荐 video_clip_duration
  - 展示图片总覆盖时长
  - 展示旁白最大中文字符数
  - 提醒 WebUI 实际 video_script 不得明显超过上限
  - 如果 WebUI 中改写文案或 AI 生成了更长文案，必须重新跑 preflight
- 当前边界：
  - 本次只修改 restaurant_docs 规格/状态文档
  - 未修改代码
  - 未修改 MoneyPrinterTurbo 原业务代码
  - 未安装依赖
  - 未调用外部 API

## Step 2-1 - validator 目标时长与动态图片数量范围校验

- 本次目标：
  - 只实现 validator 层
  - 支持 `target_duration_seconds`
  - 根据目标时长动态校验图片数量范围
  - 暂不修改 preflight/checklist 逻辑
- 允许修改：
  - restaurant_engine/models.py
  - restaurant_engine/validator.py
  - restaurant_docs/VALIDATOR_SPEC.md
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- 新增规则：
  - 合法目标时长为 30、40、50、60
  - 缺少 `target_duration_seconds` 时输出 warning，不让旧样本失败
  - 缺少时默认按 30 秒计算后续建议
  - 非法值输出 error
  - 图片太少输出 `too_few_images_for_target_duration`
  - 图片太多输出 `too_many_images_for_target_duration` warning
- 动态范围公式：
  - min_images_for_duration = ceil(target_duration_seconds / 6)
  - max_images_for_duration = floor(target_duration_seconds / 3)
  - effective_min_images = max(6, min_images_for_duration)
- 保持不变：
  - 不修改 MoneyPrinterTurbo 原业务代码
  - 不修改 preflight.py
  - 不修改 webui_checklist.py
  - 不安装依赖
  - 不调用外部 API

## Step 2-2 - preflight 目标时长动态时长计算

- 本次目标：
  - 只实现 preflight 层
  - 使用 `target_duration_seconds` 动态计算 `recommended_clip_duration`
  - 输出图片总覆盖时长和旁白字数安全上限
  - 暂不修改 validator/checklist 逻辑
- 允许修改：
  - restaurant_engine/models.py
  - restaurant_engine/preflight.py
  - restaurant_docs/PREFLIGHT_SPEC.md
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- 新增 timing 字段：
  - target_duration_seconds
  - total_image_duration
  - narration_safe_seconds
  - narration_max_cjk_chars
- 新增规则：
  - raw_clip_duration = ceil(target_duration_seconds / image_count)
  - recommended_clip_duration = clamp(raw_clip_duration, 3, 6)
  - total_image_duration = image_count * recommended_clip_duration
  - will_loop = total_image_duration < max(target_duration_seconds, estimated_narration_seconds)
- 新增 warning：
  - narration_too_long_for_target_duration
  - image_duration_shorter_than_target_duration
  - image_duration_shorter_than_narration
- 保持不变：
  - shot 顺序不变
  - video_concat_mode 仍推荐 sequential
  - video_source 仍推荐 local
  - 不修改 MoneyPrinterTurbo 原业务代码
  - 不修改 validator.py
  - 不修改 webui_checklist.py

## Step 2-3 - checklist 目标时长与文案上限展示

- 本次目标：
  - 只更新 WebUI checklist 生成器
  - 展示 preflight 新增 timing 字段
  - 强化 WebUI 最终文案一致性提示
  - 暂不修改 validator/preflight/models 逻辑
- 允许修改：
  - restaurant_engine/webui_checklist.py
  - restaurant_docs/WEBUI_CHECKLIST_SPEC.md
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- checklist 新增展示：
  - 目标视频时长
  - 当前图片数量
  - 推荐每张图片时长
  - 图片总覆盖时长
  - 旁白安全时长
  - 旁白最大中文字符数
  - WebUI 最终 `video_script` 不应明显超过上限
- 向后兼容：
  - 旧 preflight_report 缺少新增字段时显示“未提供”
  - 图片总覆盖时长可回退为图片数量 * 推荐时长
- 保持不变：
  - 不修改 MoneyPrinterTurbo 原业务代码
  - 不修改 validator.py
  - 不修改 preflight.py
  - 不修改 models.py

## Step 2-4 - WebUI 餐厅视频模式

- 本次目标：
  - 直接在 WebUI 中加入餐厅视频目标时长控制
  - 减少用户只依赖外部 checklist 手动判断导致的偏差
  - 第一版不修改视频合成核心
- 当前状态：
  - 已实现，待 WebUI 手动复测
  - 本次仅做静态检查和语法检查，未启动 WebUI
- 修改文件：
  - app/models/schema.py
  - webui/Main.py
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- VideoParams 新增字段：
  - restaurant_mode: bool = True
  - target_duration_seconds: int = 30
- WebUI 新增控件：
  - 餐厅视频模式默认开启，不再显示开关
  - 目标视频时长：30秒、40秒、50秒、60秒
  - 目标视频时长已移动到左侧文案设置区域的视频主题下方
  - 脚本语言选择隐藏，默认中文 zh-CN
- 餐厅模式下隐藏/锁定：
  - 视频来源：固定 local / 本地文件，不显示通用选择框
  - 视频拼接模式：固定 sequential / 顺序拼接，不显示通用选择框
  - 同时生成视频数量：固定 1 条，不显示通用选择框
  - 视频片段最大时长：按目标时长和图片数量自动计算，不显示通用选择框
- 餐厅模式检查：
  - 仅在 restaurant_mode=True 且 video_source=local 时启用
  - 只统计 jpg/jpeg/png 图片文件
  - 图片少于最低要求时 st.error 并阻止生成
  - 图片多于建议范围时 st.warning，不阻止生成
  - 动态推荐“视频片段最大时长(秒)”
  - 显示预计图片总覆盖时长
  - 按目标时长显示建议中文旁白长度范围
  - 文案偏短/偏长时 warning
- 生成前兜底：
  - 再次写入 restaurant_mode=True
  - 再次写入 video_language=zh-CN
  - 再次写入 video_source=local
  - 再次写入 video_concat_mode=sequential
  - 再次写入 video_count=1
  - 有图片时重新计算 video_clip_duration
- 保持不变：
  - restaurant_mode 默认开启
  - 非餐厅模式尽量保持原 WebUI 行为
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改字幕或 ffmpeg 合成逻辑
  - 不安装依赖
  - 不调用外部 API

## Step 2-5 - 餐厅模式 AI 文案长度约束

- 本次目标：
  - 修复餐厅模式下 AI 自动生成视频文案未遵守目标时长和字数范围的问题
  - 不调用外部 API 做真实生成测试
  - 不修改视频合成核心
- 修改文件：
  - webui/Main.py
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- 实现内容：
  - 新增餐厅模式文案生成 prompt 构造逻辑
  - 生成视频文案时追加目标视频时长
  - 生成视频文案时追加建议中文旁白长度范围
  - 要求 AI 不输出分镜编号、不输出解释，只输出可直接用于视频旁白的文案
  - 在 AI 生成文案按钮附近显示预计中文字符范围
- 保持不变：
  - 关键词生成仍使用原逻辑
  - 生成后仍保留文案偏短/偏长 warning
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py

## Step 2-6 - 餐厅默认流程页面精简与 AI 文案二次修正

- 本次目标：
  - 根据最新 WebUI 截图反馈精简餐厅默认流程页面
  - 把用户必须操作的内容进一步集中到左侧
  - 增强 AI 自动生成文案的目标字数符合度
- 页面调整：
  - 隐藏右侧“视频来源：本地文件（餐厅模式固定）”
  - 隐藏右侧“视频拼接模式：顺序拼接（餐厅模式固定）”
  - 隐藏右侧“同时生成视频数量：1 条（餐厅模式固定）”
  - 保留右侧上传本地文件入口
  - 视频比例移动到左侧目标视频时长下方
  - 视频比例继续写入 params.video_aspect
- AI 文案生成调整：
  - 生成后统计 CJK 中文字符数
  - 文案偏短时自动二次扩写一次
  - 文案偏长时自动二次压缩一次
  - 二次修正后仍超出推荐范围时提示手动微调
  - 关键词生成仍沿用原逻辑，不混入视频文案
- 保持不变：
  - 图片数量不足仍阻止生成
  - 文案过短/过长 warning 仍保留
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 restaurant_engine/

## Step 2-7 - AI 文案长度程序级兜底

- 本次目标：
  - 修复 40、50、60 秒目标下 AI 自动生成文案仍偏短的问题
  - 不再只依赖 prompt 或一次 AI 二次修正
  - 不调用外部 API 做真实生成测试
- 修改文件：
  - webui/Main.py
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- 实现内容：
  - 新增文案噪声清理 helper
  - 新增本地扩写 helper
  - 新增本地句子级压缩 helper
  - 新增文案长度归一化 helper
  - AI 二次修正后继续进入本地兜底
  - 偏短时追加餐厅宣传模板句补足
  - 偏长时按中文标点保留关键句并压缩
  - 关键词生成基于最终文案
- 保持不变：
  - 用户手动文案不被强制改写
  - 手动文案仍保留偏短/偏长 warning
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 app/models/schema.py
  - 不修改 restaurant_engine/

## Step 2-8 - 视频文案字数硬限制

- 本次目标：
  - 将餐厅默认流程的视频文案字数从 warning 升级为硬性生成条件
  - 不调用外部 API 做真实 AI 生成测试
  - 不修改视频合成核心
- 修改文件：
  - webui/Main.py
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- 实现内容：
  - 新增 `clamp_script_to_max_cjk_chars(...)`
  - 视频文案输入框下方显示当前中文字符数和目标范围
  - 目标时长变化后自动切换 30/40/50/60 秒对应的字数范围
  - 手动输入或粘贴超过最大中文字符数时自动截断
  - 文案低于最小中文字符数时显示缺口
  - 文案合格时显示可生成状态
  - 生成按钮仅在文案字数合格且图片数量满足最低要求时可用
  - 点击生成前保留最终兜底检查，确保不绕过字数和图片数量限制
  - AI 生成文案后同样进入归一化和最大字数截断
  - 关键词继续基于最终文案生成
- 保持不变：
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 restaurant_engine/
  - 不安装依赖
  - 不调用外部 API

## Step 2-9 - 视频比例移动到中间列上传模块上方

- 本次目标：
  - 根据最新布局要求，将视频比例从左侧文案设置区域移动到中间列上传本地文件模块上方
  - 不修改视频合成核心
- 修改文件：
  - webui/Main.py
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- 实现内容：
  - 左侧文案设置区域移除视频比例控件
  - 中间列餐厅默认流程中，在上传本地文件之前显示视频比例控件
  - 视频比例仍提供竖屏 9:16 和横屏 16:9
  - 默认仍为 9:16
  - 继续写入 `params.video_aspect`
- 保持不变：
  - 视频来源固定 local 且隐藏
  - 视频拼接模式固定 sequential 且隐藏
  - 视频片段最大时长继续自动计算
  - 同时生成视频数量固定 1
  - 图片数量不足时仍阻止生成
  - 文案字数不符合要求时仍阻止生成
  - 不修改 app/models/schema.py
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 restaurant_engine/

## Step 2-10 - 禁用 Streamlit Clear caches 弹窗入口

- 本次目标：
  - 定位 WebUI 复制操作时弹出 `Clear caches` 窗口的来源
  - 做最小修复，不修改视频合成核心
- 定位结果：
  - 未在项目代码中发现自定义 `Clear caches` 弹窗
  - 未发现自定义 clipboard / copy JS 事件绑定
  - `Clear caches` 最可能来自 Streamlit 内置菜单或 toolbar
- 修改文件：
  - webui/Main.py
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- 实现内容：
  - 将 `st.set_page_config(...)` 的 `Get Help`、`Report a bug`、`About` 菜单项置空
  - 通过 CSS 隐藏 Streamlit 内置 `MainMenu`
  - 通过 CSS 隐藏 Streamlit toolbar、Deploy 按钮、状态入口和 decoration
- 保持不变：
  - 不修改复制文本本身
  - 不修改上传本地文件功能
  - 不修改餐厅默认流程逻辑
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 restaurant_engine/

## Step 2-11 - 隐藏左侧脚本语言提示和高级脚本设置

- 本次目标：
  - 继续精简 WebUI 左侧文案设置区域
  - 隐藏脚本语言提示
  - 隐藏高级脚本设置
  - 不修改视频合成核心
- 修改文件：
  - webui/Main.py
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- 实现内容：
  - 移除左侧 `脚本语言：中文（餐厅视频流程默认）` 页面提示
  - 移除左侧 `高级脚本设置` expander
  - 后台继续写入 `video_language=zh-CN`
  - 后台使用默认 `paragraph_number=1`
  - 后台使用空 `video_script_prompt`
  - 后台使用空 `custom_system_prompt`
- 保持不变：
  - AI 生成视频文案按钮保留
  - 视频文案输入框保留
  - 视频关键词输入框保留
  - 视频比例仍在中间列上传本地文件上方
  - 不修改 app/models/schema.py
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 restaurant_engine/

## Step 2-12 - 隐藏中间列详细字数和视频片段说明

- 本次目标：
  - 继续精简 WebUI 中间列素材上传区域
  - 隐藏详细字数提示和解释型视频片段说明
  - 不修改视频合成核心
- 修改文件：
  - webui/Main.py
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- 实现内容：
  - 中间列不再显示 `建议中文旁白长度：X-Y 个中文字符`
  - 中间列不再显示 `当前文案中文字符数：N`
  - 中间列不再显示 `WebUI 的视频片段最大时长不是最终视频总时长` 说明
  - 文案不合格时保留简短 warning
- 保持不变：
  - `min_chars` / `max_chars` / `cjk_count` 仍继续计算
  - `script_length_ok` / `can_generate` 仍继续控制生成按钮
  - 超长自动截断仍保留
  - 低于最小字数时仍禁用/阻止生成
  - 图片数量不足仍阻止生成
  - 不修改 app/models/schema.py
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 restaurant_engine/

## Step 2-13 - 视频文案输入框输入态自动截断

- 本次目标：
  - 修复视频文案输入框在输入态超出字数后仍显示超出内容的问题
  - 不修改视频合成核心
- 修改文件：
  - webui/Main.py
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- 实现内容：
  - 视频文案输入框改为绑定 `video_script_input` session key
  - 新增 `sync_video_script_input(...)`
  - 后端统计 CJK 中文字符数，保留最大字数兜底
  - 超过最大中文字符数时调用 `clamp_script_to_max_cjk_chars(...)`
  - 截断结果同步写回 `video_script`
  - 字数显示基于最终可生成文案
- 保持不变：
  - 低于最小字数时仍禁用/阻止生成
  - 图片数量不足仍阻止生成
  - AI 自动生成文案仍走最大字数限制
  - 不修改 app/models/schema.py
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 restaurant_engine/

## Step 2-14 - 视频文案微博式输入框限制

- 本次目标：
  - 按新浪微博输入框体验重新实现视频文案字数限制
  - 达到最大中文字符数后继续输入中文不进入输入框
  - 粘贴超长内容时只接收允许范围内的部分
  - 不以 `输入后 rerun 截断` 作为主要方案
- 修改文件：
  - webui/Main.py
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- 实现内容：
  - 保留 Streamlit 原生 `st.text_area` 和 `video_script_input` session key
  - 通过 `st.components.v1.html` 注入浏览器端 JS，不新增依赖
  - 前端监听 `beforeinput`，超过最大 CJK 字符数时阻止继续输入
  - 前端监听 `paste`，粘贴超长内容时只插入可保留部分
  - 前端监听 `input`，实时更新字数状态并作为浏览器端兜底
  - 字数状态显示 `还差 X 字`、`还可输入 Y 字`、`已达上限`
  - 输入框值继续同步到 `params.video_script`
- 保持不变：
  - 低于最小字数时仍禁用/阻止生成
  - 图片数量不足仍阻止生成
  - 后端生成前仍保留字数和图片数量兜底
  - AI 自动生成文案仍走最大字数限制
  - 不修改 app/models/schema.py
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 restaurant_engine/

## Step 2-15 - Clear caches 弹窗再次处理

- 本次目标：
  - 优先修复 WebUI 复制操作时反复弹出 `Clear caches` 窗口的问题
  - 先定位来源，再做最小修复
  - 不修改视频合成核心
- 修改文件：
  - webui/Main.py
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- 定位结果：
  - 未发现项目自定义 `Clear caches` 文案或按钮
  - 未发现项目自定义 copy / clipboard 复制事件绑定
  - 视频文案输入框中的 `clipboardData` 仅用于 paste 限制，不监听 copy
  - 最可能来源仍是 Streamlit 内置 header / toolbar / menu
- 实现内容：
  - 加固 `streamlit_style` 中对 Streamlit 内置菜单的隐藏规则
  - 隐藏 `#MainMenu`
  - 隐藏 `[data-testid="stMainMenu"]`
  - 隐藏 `[data-testid="stHeader"]`
  - 隐藏 `[data-testid="stToolbar"]`
  - 隐藏 `[data-testid="stDeployButton"]`
  - 隐藏 `[data-testid="stAppDeployButton"]`
  - 隐藏 `.stDeployButton`
  - 隐藏 `header` 及常见 Main menu / Deploy 按钮入口
- 保持不变：
  - 浏览器正常复制能力保留
  - 上传文件功能不变
  - 餐厅默认流程逻辑不变
  - 不修改 app/models/schema.py
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 restaurant_engine/

## Step 2-16 - AI 生成按钮文案精简

- 本次目标：
  - 将左侧 AI 生成按钮文案统一改为 `AI生成视频文案`
  - 不修改按钮功能逻辑
  - 不修改视频合成核心
- 修改文件：
  - webui/i18n/zh.json
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- 实现内容：
  - 将中文翻译 `Generate Video Script and Keywords` 从长说明改为 `AI生成视频文案`
  - `webui/Main.py` 仍使用原 translation key 和原按钮 key `auto_generate_script`
  - AI 生成视频文案逻辑保持不变
  - 如当前逻辑仍生成视频关键词，则继续保持不变
- 保持不变：
  - 餐厅模式字数约束不变
  - AI 二次修正和本地兜底不变
  - 不修改 app/models/schema.py
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 restaurant_engine/

## Step 2-17 - AI 文案与关键词前台流程精简

- 本次目标：
  - 前台只保留一个 `AI生成视频文案` 按钮
  - 点击按钮后自动完成视频文案生成和关键词生成
  - 隐藏独立关键词生成按钮
  - 隐藏视频关键词标题和输入框
  - 不修改视频合成核心
- 修改文件：
  - webui/Main.py
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- 实现内容：
  - 餐厅默认流程下隐藏 `Generate Video Keywords` 按钮
  - 餐厅默认流程下隐藏 `Video Keywords` 输入框
  - `AI生成视频文案` 按钮生成文案后，继续自动调用关键词生成
  - 关键词生成基于字数约束、二次修正、本地兜底后的最终文案
  - 关键词生成成功后写入 `st.session_state["video_terms"]` 和 `params.video_terms`
  - 关键词生成失败时不阻断文案生成，显示 warning
  - 关键词为空时使用本地默认关键词兜底
  - 用户手动修改文案时不自动调用关键词 API
  - 点击生成视频时不额外调用关键词 API；如关键词为空，先写入本地默认关键词
- 保持不变：
  - `params.video_terms` 字段保留
  - 餐厅模式字数约束不变
  - AI 二次修正和本地文案兜底不变
  - 不修改 app/models/schema.py
  - 不修改 app/services/task.py
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 restaurant_engine/

## Step 2-18 - Clear caches 弹窗强制抑制

- 本次目标：
  - 彻底修复 WebUI 复制文本时反复弹出 `Clear caches` 窗口的问题
  - 正常复制文本不受影响
  - 不删除缓存机制本身
  - 不修改视频合成核心
- 修改文件：
  - webui/Main.py
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- 定位结果：
  - 未发现项目自定义 `Clear caches` 文案或按钮
  - 未发现项目自定义 copy / clipboard 复制事件绑定
  - 当前视频文案输入框的 `clipboardData` 仅用于 paste 限制，不监听 copy
  - 最可能来源是 Streamlit 内置 toolbar / menu / cache 弹窗
- 实现内容：
  - 新增集中 helper `hide_streamlit_dev_chrome_and_cache_popup()`
  - helper 在 `st.set_page_config(...)` 后立即调用
  - 统一隐藏 Streamlit 顶部菜单、toolbar、deploy、status、decoration 入口
  - 注入 `MutationObserver` 监听 DOM 变化
  - 如果出现 `Clear cache`、`Clear caches`、`Clear Cache`、`Clear Caches`、`清除缓存` 文案，自动隐藏最近的 modal / popover / menu 容器
- 保持不变：
  - 不拦截 Ctrl+C / Cmd+C
  - 不拦截普通复制操作
  - 不删除或禁用 `st.cache_data`
  - 不修改 app/models/schema.py
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 restaurant_engine/

## Step 2-19 - WebUI 品牌显示调整

- 本次目标：
  - 将 WebUI 页面左上角 `MoneyPrinterTurbo v1.2.9` 替换为 `TwinkleBite AI`
  - 只做品牌显示文案替换
  - 不做全局项目名替换
- 修改文件：
  - webui/Main.py
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- 实现内容：
  - `st.set_page_config(...)` 的 `page_title` 改为 `TwinkleBite AI`
  - 左上角 `st.title(...)` 改为 `TwinkleBite AI`
  - 不再显示 `v1.2.9` 版本后缀
- 保持不变：
  - 不替换项目路径中的 `MoneyPrinterTurbo`
  - 不替换 Python 包名
  - 不替换 Git 仓库名
  - 不改历史文档记录
  - 不修改 app/models/schema.py
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 restaurant_engine/

## Step 2-20 - Cmd+C 页面空白稳定性修复

- 本次目标：
  - 修复 WebUI 中连按 `Cmd+C` 复制导致页面空白的问题
  - 优先恢复页面稳定性
  - 暂不继续强制删除 `Clear caches` 弹窗 DOM
  - 不修改视频合成核心
- 修改文件：
  - webui/Main.py
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- 定位结果：
  - `webui/Main.py` 中存在 `hide_streamlit_dev_chrome_and_cache_popup()`
  - 该 helper 内包含全局 `MutationObserver`
  - 该逻辑会扫描包含 `Clear cache(s)` 文案的 `div`、`modal`、`popover`、`menu` 等节点并隐藏容器
  - 该策略过于激进，可能误伤 Streamlit 页面主体，导致复制后页面空白
- 实现内容：
  - 移除 `MutationObserver` DOM 监听和弹窗容器隐藏逻辑
  - 移除 `Clear cache(s)` 文案扫描逻辑
  - 保留最小 Streamlit 菜单 CSS 隐藏：
    - `#MainMenu`
    - `[data-testid="stToolbar"]`
    - `[data-testid="stStatusWidget"]`
    - `.stDeployButton`
  - 删除/避免隐藏高风险选择器：
    - `header`
    - `[data-testid="stDecoration"]`
    - `[data-testid="baseButton-header"]`
- 保持不变：
  - 不拦截 `Cmd+C` / `Ctrl+C`
  - 不监听 `copy` 事件
  - 不修改 app/models/schema.py
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 restaurant_engine/

## Step 2-21 - Clear caches 快捷键精确拦截

- 本次目标：
  - 在不恢复全局 DOM 扫描的前提下，继续降低 `Clear caches` 弹窗触发概率
  - 保留普通复制功能
  - 不修改视频合成核心
- 修改文件：
  - webui/Main.py
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- 定位结果：
  - 当前 `webui/Main.py` 中已无全局 `MutationObserver`
  - 当前没有自定义 `copy` 监听
  - 当前没有 `keydown` / `keyup` / `keypress` 监听
- 实现内容：
  - 在 `hide_streamlit_dev_chrome_and_cache_popup()` 中新增精确 keyboard guard
  - 通过 capture phase 监听父页面 `keydown`
  - 普通 `Cmd+C` / `Ctrl+C` 不拦截
  - 仅拦截非输入区域的 `Cmd/Ctrl + Shift/Alt + C` 组合
  - 拦截时调用 `preventDefault()`、`stopPropagation()`、`stopImmediatePropagation()`
  - 在 `input`、`textarea`、`contenteditable` 内绝不拦截
- 保持不变：
  - 不使用全局 `MutationObserver`
  - 不扫描或隐藏页面 `div` / `section` / `modal` / `popover`
  - 不监听 `copy` 事件
  - 继续保留最小 Streamlit toolbar/menu CSS 隐藏
  - 不修改 app/models/schema.py
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 restaurant_engine/

## Step 2-22 - Clear caches 原生弹窗精确抑制

- 本次目标：
  - 修复普通 `Cmd+C` 连按后仍出现 Streamlit 原生 `Clear caches` dialog 的问题
  - 不恢复全局 DOM 扫描
  - 不影响页面稳定性和正常复制
  - 不修改视频合成核心
- 修改文件：
  - webui/Main.py
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- 定位结果：
  - 用户截图确认弹窗是 Streamlit 原生 `Clear caches` dialog
  - 弹窗包含 `Are you sure you want to clear the app's function caches?`
  - 之前 keyboard guard 不能覆盖普通 `Cmd+C` 连按触发场景
- 实现内容：
  - 新增精确 `Clear caches` dialog guard
  - 使用 `MutationObserver`，但只检查 dialog / modal 候选
  - 候选选择器仅包含：
    - `[role="dialog"]`
    - `[data-baseweb="modal"]`
    - `[data-testid="stModal"]`
    - `[data-testid*="Modal"]`
  - 只有候选元素同时包含 `Clear caches` 和缓存确认文案时才处理
  - 优先点击 `Cancel`
  - 找不到 `Cancel` 时尝试点击 close/cancel 类按钮
  - 仅在找不到关闭按钮时隐藏该 dialog 容器
- 保持不变：
  - 不扫描全页面 `div` / `section`
  - 不隐藏整个 `header`
  - 不隐藏整个 app 容器
  - 不监听普通 `copy` 事件
  - 普通 `Cmd+C` / `Ctrl+C` 复制不拦截
  - 继续保留最小 Streamlit toolbar/menu CSS
  - 不修改 app/models/schema.py
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 restaurant_engine/

## Step 2-23 - WebUI 餐厅默认流程收口

- 本次目标：
  - 对当前未提交的 WebUI 餐厅默认流程改造做最终提交前收口
  - 记录用户已确认 `Clear caches` 复制阻塞问题已解决
  - 准备提交本轮 WebUI 改造
- 修改文件：
  - app/models/schema.py
  - webui/Main.py
  - webui/i18n/zh.json
  - restaurant_docs/PROJECT_STATUS.md
  - restaurant_docs/TASK_LOG.md
- 已完成能力：
  - WebUI 品牌显示为 `TwinkleBite AI`
  - 餐厅默认流程开启
  - 目标视频时长 30 / 40 / 50 / 60 秒
  - 本地文件、顺序拼接、单条生成、动态片段时长均由餐厅流程锁定
  - 视频比例移动到中间列上传本地文件模块上方
  - 左侧只保留必要文案流程
  - `AI生成视频文案` 按钮自动生成文案并基于最终文案生成关键词
  - 隐藏独立关键词生成按钮和关键词输入框
  - `params.video_terms` 仍保留并自动写入
  - 文案字数和图片数量共同控制生成按钮
  - 精确 `Clear caches` dialog guard 已加入，并经用户反馈确认解决阻塞问题
- 保持不变：
  - 不修改 app/services/video.py
  - 不修改 app/services/voice.py
  - 不修改 app/services/subtitle.py
  - 不修改 config.toml
  - 不修改 restaurant_engine/
  - 不提交 storage/ 生成产物
  - 不提交 validation_report.json / preflight_report.json / webui_checklist.md
  - 不提交 .pyc / __pycache__/

## Step 2-24 - TwinkleBite AI WebUI 初版里程碑记录

- 本次目标：
  - 记录 `TwinkleBite AI` 默认餐厅视频 WebUI 初版完成状态
  - 只更新项目文档
  - 不修改代码
- 关联提交：
  - `f287eb85c5131dc305bf6e5d651d4b2161e3839a`
  - `feat: add default restaurant video WebUI workflow`
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

## 多样本完整生成测试记录

测试目标：
- 验证 TwinkleBite AI 默认餐厅 WebUI 流程在多个真实餐厅样本上可稳定生成视频。
- 验证目标时长、图片覆盖、顺序拼接、字幕/语音同步、隐藏关键词流程是否稳定。
- 本阶段由用户在浏览器中手动生成视频；Codex 不主动触发外部 API，不主动生成视频。

样本检查结果：
- `hotpot_001`：8 张图片，存在 `project.json`
  - `01_intro.jpg`
  - `02_interior.jpg`
  - `03_dish_1.jpg`
  - `04_dish_2.jpg`
  - `05_dining.jpeg`
  - `06_extra.jpg`
  - `07.jpg`
  - `08.jpeg`
- `sichuan_001`：6 张图片，存在 `project.json`
  - `01_intro.jpg`
  - `02_interior.jpg`
  - `03_dish_1.jpg`
  - `04_dish_2.jpg`
  - `05_dining.jpeg`
  - `06_extra.jpg`
- 第三个真实餐厅样本：当前缺失，待补充一个至少 8 张图片的真实餐厅样本。

当前测试矩阵：

| Case | 样本 | 目标时长 | 图片数量 | 状态 | final mp4 | 主要观察 |
|---|---|---:|---:|---|---|---|
| A | hotpot_001 | 30 秒 | 8 | 通过 | 待补充 | 整数秒 per-image duration 生效；8 张图全部出现，无重复，顺序正确，成片 30 秒 |
| B | sichuan_001 | 30 秒 | 6 | 通过 | 待补充 | 30 秒 / 6 图整数秒分配正常；6 张图全部出现，无重复，顺序正确，成片 30 秒 |
| C | 第三个真实餐厅样本（火锅店样本） | 40 秒 | 8 | 通过 | 待补充 | 40 秒 / 8 图整数秒分配正常；8 张图全部出现，无重复，顺序正确，成片 40 秒 |
| D | 真实餐厅样本 | 50 秒 | 10 | 通过 | 待补充 | 已测试，暂未发现问题 |
| E | 真实餐厅样本 | 60 秒 | 12 | 通过 | 待补充 | 已测试，暂未发现问题 |

单个样本检查项：
- 图片是否全部出现：
- 是否重复图片：
- 图片顺序是否正确：
- 成片时长：
- 字幕是否出现：
- 字幕/语音是否同步：
- BGM 是否正常：
- 页面是否报错：
- 生成任务路径：
- 结论：

手动 WebUI 测试步骤：
1. 打开 WebUI：`http://127.0.0.1:8501`
2. 设置目标视频时长：30 秒或 40 秒。
3. 上传该样本目录内所有图片，按文件名顺序选择。
4. 检查页面是否显示图片数量足够。
5. 输入或粘贴符合字数范围的视频文案。
6. 不要点击外部 API 相关按钮，除非用户明确要测试 `AI生成视频文案`。
7. 点击生成视频。
8. 等待任务完成。
9. 记录 final mp4 路径。
10. 人工打开视频检查：图片是否全部出现、是否重复图片、图片顺序是否正确、成片时长是否接近目标、字幕是否出现、字幕和语音是否同步、BGM 是否正常、页面是否报错。

说明：
- 如需测试 `AI生成视频文案` 按钮，会调用外部 API，必须由用户本人手动点击。
- Codex 本次未修改业务代码，未调用外部 API，未生成视频，未提交。

## Case A 30 秒 hotpot_001 复测问题与修复准备

- 用户手动复测结果：
  - 样本：`hotpot_001`
  - 目标时长：30 秒
  - 上传图片数量：8 张
  - 生成视频时长约 28 秒
  - 图片顺序正确、没有重复、字幕/语音/BGM 正常
  - 第 8 张图片未出现
- 问题判断：
  - 旧逻辑仍以单一 `video_clip_duration` 表示每段最大时长。
  - 8 张图、目标 30 秒时，固定 4 秒会得到 32 秒覆盖能力，但合成阶段会按音频时长提前停止，导致尾部图片可能被截掉。
  - 当前餐厅模式需要按目标总时长和图片数量生成每张图的整数秒时长列表。
- 本次修复方向：
  - 新增 `video_clip_durations` 参数用于表示每张图片展示时长。
  - 餐厅模式按目标时长和图片数量动态分配整数秒片段。
  - 示例：30 秒 / 8 张图 => `[4, 4, 3, 4, 4, 3, 4, 4]`，总和 30 秒。
  - 本地图片预处理和合成阶段优先使用 `video_clip_durations`。
  - 合成阶段收到完整 per-image 时长列表时，以列表总和作为目标覆盖时长，避免短音频提前截断尾部图片。
- 当前边界：
  - 不修改 TTS、字幕、BGM、ffmpeg 核心能力。
  - 不提交生成产物。
  - 本次完成后仍需用户重启 WebUI 并重新做 hotpot_001 Case A 手动复测。

## Case A 30 秒 hotpot_001 整数秒片段复测结论

- Case A 初测问题：
  - 样本：`hotpot_001`
  - 目标时长：30 秒
  - 图片数量：8 张
  - 初测生成视频约 28 秒
  - 第 8 张图片未出现
  - 原因判断：旧逻辑仍按固定/最大片段时长计算，最终合成受音频时长提前停止影响，尾部图片被截掉。
- 修复内容：
  - 新增 `video_clip_durations` 参数。
  - 餐厅模式按目标总时长和图片数量生成整数秒片段列表。
  - 所有片段均为整数秒。
  - 所有片段总和等于目标时长。
  - 余数均匀分配到图片序列中。
  - `30 秒 / 8 张图 = 4, 4, 3, 4, 4, 3, 4, 4 秒`。
- 用户复测结果：
  - 页面显示整数片段列表：是。
  - 页面显示的片段列表：`4, 4, 3, 4, 4, 3, 4, 4 秒`。
  - 页面显示的覆盖时长：30 秒。
  - 成片时长：30 秒。
  - 8 张图片是否全部出现：是。
  - 是否重复图片：否。
  - 图片顺序是否正确：是。
  - 字幕是否出现：是。
  - 字幕/语音是否同步：是。
  - BGM 是否正常：是。
  - 页面是否报错：否。
- 结论：
  - Case A 通过。
  - 整数秒 per-image duration 修复有效，解决了第 8 张图片未出现的问题。

## Case B 30 秒 sichuan_001 完整流程复测结论

- 用户手动测试结果：
  - 样本：`sichuan_001`
  - 目标时长：30 秒
  - 图片数量：6 张
  - 页面是否显示整数片段列表：是。
  - 页面显示的片段列表：`5, 5, 5, 5, 5, 5 秒`。
  - 页面显示的覆盖时长：30 秒。
  - 成片时长：30 秒。
  - 6 张图片是否全部出现：是。
  - 是否重复图片：无。
  - 图片顺序是否正确：是。
  - 字幕是否出现：是。
  - 字幕/语音是否同步：是。
  - BGM 是否正常：是。
  - 页面是否报错：无。
- 结论：
  - Case B 通过。
  - 30 秒 / 6 张图片的整数秒片段分配正常。
  - 完整生成流程稳定。
- 当前多样本验证状态：
  - `hotpot_001`：30 秒 / 8 图，通过。
  - `sichuan_001`：30 秒 / 6 图，通过。
- 下一步建议：
  - 补充第三个真实餐厅样本，至少 8 张图片。
  - 测试 40 秒流程，重点确认自动分配、图片覆盖、字幕/语音同步和成片稳定性。

## Case C 40 秒第三个真实餐厅样本复测结论

- 用户手动测试结果：
  - 样本：第三个真实餐厅样本，火锅店样本。
  - 目标时长：40 秒。
  - 图片数量：8 张。
  - 页面是否显示整数片段列表：是。
  - 页面显示的片段列表：`5, 5, 5, 5, 5, 5, 5, 5 秒`。
  - 页面显示的覆盖时长：40 秒。
  - 成片时长：40 秒。
  - 8 张图片是否全部出现：是。
  - 是否重复图片：无。
  - 图片顺序是否正确：是。
  - 字幕是否出现：是。
  - 字幕/语音是否同步：是。
  - BGM 是否正常：是。
  - 页面是否报错：无。
- 结论：
  - Case C 通过。
  - 40 秒 / 8 张图片流程稳定，整数秒片段分配正常。
- 当前多样本验证总结：
  - 30 秒 / 8 图：通过。
  - 30 秒 / 6 图：通过。
  - 40 秒 / 8 图：通过。
- 当前结论：
  - `TwinkleBite AI` 餐厅视频默认 WebUI 主流程已完成 30 秒与 40 秒真实样本验证。
  - 整数秒图片片段分配逻辑通过多样本测试。
- 下一步建议：
  - 后续可继续测试 50 秒 / 10 图、60 秒 / 12 图。
  - 暂停继续改核心逻辑，优先沉淀使用说明和样本规范。

## 50 秒 / 10 图与 60 秒 / 12 图补充测试记录

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

## WebUI 后台启动脚本实现记录

- 本次目标：
  - 增加 TwinkleBite AI WebUI 后台启动、停止、状态检查脚本。
  - 让用户在本机 macOS 上可后台启动 WebUI，关闭终端后尽量保持运行。
  - 本次只做实现和静态检查，暂不自动启动或停止 WebUI。
- 新增脚本：
  - `scripts/twinkle_webui_start.sh`
  - `scripts/twinkle_webui_stop.sh`
  - `scripts/twinkle_webui_status.sh`
- 运行文件：
  - `.runtime/twinkle_webui.pid`
  - `.runtime/twinkle_webui.log`
  - `.runtime/` 已加入 `.gitignore`。
- 使用方式：
  - `scripts/twinkle_webui_start.sh`
  - `scripts/twinkle_webui_status.sh`
  - `scripts/twinkle_webui_stop.sh`
- 行为说明：
  - start 默认端口为 8501，端口已占用时拒绝启动，不强杀。
  - stop 读取 PID 文件并使用普通 `kill` 温和停止，最多等待 5 秒，不默认 `kill -9`。
  - status 输出 PID 文件状态、PID 是否运行、端口监听、WebUI URL 和最近 40 行日志。
- 用户手动验证结果：
  - start：成功。
  - 关闭终端后：WebUI 仍保持运行。
  - status：能看到 PID 正在运行、8501 正在监听。
  - stop：成功。
  - stop 后：PID file exists: no。
  - stop 后：8501 无 listener。
- 当前边界：
  - 未修改业务代码。
  - 未修改 WebUI 功能逻辑。
  - 未修改视频生成核心。

## AI 生成视频文案按钮稳定性测试记录

测试目标：
- 验证 `AI生成视频文案` 按钮在不同目标时长下能否稳定调用外部 API。
- 验证生成文案是否自动写入视频文案框。
- 验证生成文案是否满足目标时长对应的中文字符范围。
- 验证隐藏关键词流程是否不影响用户操作。
- 本轮不测试视频生成，不主动生成视频。

| Case | 目标时长 | 视频主题 | 推荐字数范围 | 是否成功返回 | 返回耗时 | 实际中文字符数 | 是否合规 | 页面/API 报错 | 备注 |
|---|---:|---|---|---|---:|---:|---|---|---|
| AI-A | 30 秒 | 四川火锅宣传 | 96-108 | 是 | 待补充 | 102 | 是 | 无 | 通过，已自动填入视频文案框 |
| AI-B | 40 秒 | 重庆老火锅门店探店 | 136-148 | 是 | 待补充 | 148 | 是 | 无 | 通过，已自动填入视频文案框 |
| AI-C | 60 秒 | 川菜馆招牌菜推荐 | 216-228 | 是 | 待补充 | 226 | 是 | 无 | 通过，已自动填入视频文案框 |

单次测试记录项：
- 是否成功返回文案：
- 返回耗时：
- 实际中文字符数：
- 是否落在推荐范围：
- 是否自动填入视频文案框：
- 是否出现页面报错：
- 是否出现 API 报错：
- 是否需要重试：
- 结论：

补充结论：
- `AI生成视频文案` 按钮已完成 30 / 40 / 60 秒手动测试。
- 三次测试均成功返回文案。
- 三次测试均自动填入视频文案框。
- 生成文案均落在目标时长推荐字数范围内：
  - 30 秒：102 / 96-108。
  - 40 秒：148 / 136-148。
  - 60 秒：226 / 216-228。
- 页面/API 暂未发现报错。
- 当前结论：
  - AI 文案按钮外部 API 稳定性初步通过。
  - 字数控制和自动压缩/长度兜底逻辑有效。
  - 隐藏关键词流程未影响用户操作。
- 当前 MVP 已验证范围：
  - 30 / 40 / 50 / 60 秒视频主流程通过。
  - AI 文案按钮 30 / 40 / 60 秒通过。
- 后续建议：
  - 后续可补测 50 秒 AI 文案。
  - 后续可测试更多主题风格。
  - 暂停改核心逻辑。

## WebUI 页面精简与样式清理第一轮

- 本次目标：
  - 精简 WebUI 页面中普通用户不需要看的技术提示和样式噪音。
  - 让页面更偏向餐厅短视频产品体验。
- 调整内容：
  - `视频主题` 标签去掉技术性括号说明。
  - 增加简短说明：输入餐厅名称、菜品类型或推广主题。
  - `目标视频时长` 增加简短说明：系统会按目标时长控制文案字数和图片展示节奏。
  - `视频文案` 标签去掉长括号说明。
  - 增加简短说明：可手动填写，也可使用 AI 生成。建议使用自然标点，字幕效果更稳定。
  - AI 文案生成后的扩写、压缩、截断提示改为更短表述。
  - 中间列自动分配提示改为：系统会根据目标时长和图片数量自动分配每张图片的展示时间。
  - API Key 折叠入口文案改为 `API Key 管理`。
- 保持不变：
  - 目标时长选择。
  - 图片上传。
  - 整数秒片段分配显示。
  - 文案字数校验。
  - `AI生成视频文案` 按钮。
  - 字幕设置。
  - 音频设置。
  - 视频生成核心。
  - 后台启动脚本。

## WebUI 朗读声音选项精简

- 本次目标：
  - 在餐厅视频默认流程中精简 `朗读声音` 下拉列表。
  - 普通用户只看到 `zh-CN` 中文普通话声音。
- 调整内容：
  - 在 WebUI 展示层过滤声音列表，只保留名称中包含 `zh-CN` 的声音。
  - 默认声音优先选择 `zh-CN-XiaoxiaoNeural` 系列。
  - 如果 `zh-CN-XiaoxiaoNeural` 不存在，则回退到第一个 `zh-CN` 声音。
  - `朗读声音` 标签去掉技术性说明，附近改为简短产品说明：当前仅开放中文普通话声音，适合餐厅短视频旁白。
  - 如果当前 TTS 配置没有 `zh-CN` 声音，页面提示检查 TTS 声音配置，不再自动展示非中文声音。
  - 朗读声音下拉框用户可见标签去掉 `zh-CN-` 前缀。
  - 朗读声音下拉框用户可见性别标签统一为 `男声` / `女声`，不再显示 `男性` / `女性`。
  - 下拉框仍使用原始完整 `voice_name` 作为实际选中值，避免影响 TTS 生成。
  - 隐藏 `音频设置` 中的 TTS 服务器选择模块及其说明文字。
  - 底层仍沿用当前默认 TTS server 配置；配置无效时回退到 `azure-tts-v1`。
  - 隐藏 `朗读音量`、`朗读速度`、`自定义音频文件` 模块。
  - 底层仍使用默认朗读音量 `1.0`、朗读速度 `1.0`，且不使用自定义音频文件。
  - 保留 `朗读声音` 下拉框和背景音乐设置。
  - `朗读声音` 字段去掉与文案语言、API Key 相关的技术说明，只保留简洁标签。
  - 背景音乐下拉框隐藏 `自定义背景音乐` 选项，普通用户只选择内置/随机/无背景音乐。
  - 底层自定义 BGM 能力不删除，背景音乐音量设置保留。
  - 浏览器确认发现 `背景音乐音量` 控件仍显示，本轮已隐藏该控件。
  - 底层仍使用默认背景音乐音量 `0.2`，不影响背景音乐混音。
- 保持不变：
  - 未修改 `app/services/voice.py`。
  - 未删除底层 TTS 多语言能力。
  - 未修改视频生成核心。
  - 未修改后台脚本。

## 背景音乐精选命名准备

- 本次目标：
  - 为 `resource/songs/` 内置背景音乐建立试听和命名清单。
  - 先让用户试听确认名称，不直接修改 WebUI 下拉框。
- 新增内容：
  - `restaurant_docs/BGM_CATALOG.md`
  - `scripts/twinkle_bgm_preview.sh`
- 记录范围：
  - 覆盖 `output000.mp3` 到 `output025.mp3`。
  - 覆盖 `output027.mp3` 到 `output029.mp3`。
  - 记录 `output026.mp3` 缺失。
- 试听脚本能力：
  - `scripts/twinkle_bgm_preview.sh list`：列出可试听 BGM。
  - `scripts/twinkle_bgm_preview.sh output000.mp3`：默认试听 20 秒。
  - `scripts/twinkle_bgm_preview.sh output000.mp3 20`：试听指定秒数。
- 当前边界：
  - 未修改 WebUI 逻辑。
  - 未修改视频生成核心。
  - 未播放音频。
  - 等用户试听后再确认精选名称和 WebUI 接入方式。

## WebUI 视频设置继续精简

- 本次目标：
  - 隐藏餐厅默认流程中普通用户不需要调整的视频高级控件。
- 调整内容：
  - 隐藏 `视频转场模式` 控件。
  - 底层继续使用 `无转场`。
  - 隐藏 `高级视频设置` expander。
  - 底层继续沿用当前默认高级视频参数。
  - 隐藏未上传图片时的 `上传图片后自动计算每张图片展示时长` 蓝色提示。
- 保持不变：
  - 视频比例。
  - 上传本地文件。
  - 图片数量提示。
  - 每张图片展示时长。
  - 预计图片总覆盖时长。
  - 整数秒片段分配。
  - 图片数量校验和生成前拦截。
  - 文案字数校验。
  - 生成视频按钮。
  - 视频生成核心。
  - 后台脚本。

## WebUI 字幕设置布局纠正

- 本次目标：
  - 纠正上一轮字幕设置放置位置。
  - `字幕设置` 应位于中间列 `音频设置` 下方，而不是图片数量信息下方。
- 调整内容：
  - 将字幕设置从右侧独立列移除。
  - 将字幕设置放到中间列音频设置模块下方。
  - 保持字幕设置只渲染一次。
- 保持不变：
  - 启用字幕。
  - 字幕字体、位置、颜色、大小。
  - 描边颜色、描边粗细。
  - 字幕背景、圆角半透明字幕背景。
  - `app/services/subtitle.py`。
  - 字幕生成逻辑。
  - 视频生成核心。

## WebUI 字幕设置继续精简

- 本次目标：
  - 进一步精简中间列字幕设置区域。
  - 普通用户只需要看到 `启用字幕` 开关。
- 调整内容：
  - 隐藏字幕字体、字幕位置、字幕颜色、字幕大小。
  - 隐藏描边颜色、描边粗细。
  - 隐藏字幕背景与圆角半透明字幕背景控件。
  - 保留 `启用字幕` checkbox。
  - 底层默认使用 `STHeitiMedium.ttc`、底部、白色、字号 `50`、黑色描边 `1.5`。
  - 底层默认关闭字幕背景和圆角半透明字幕背景。
- 保持不变：
  - 用户取消 `启用字幕` 时仍会关闭字幕。
  - `app/services/subtitle.py`。
  - 字幕生成逻辑。
  - 视频生成核心。

## WebUI 视频片段明细展示隐藏

- 本次目标：
  - 继续精简视频设置区域。
  - 上传图片后不再向普通用户展示片段分配明细。
- 调整内容：
  - 隐藏 `每张图片展示时长`。
  - 隐藏 `预计图片总覆盖时长`。
  - 隐藏自动分配展示时间说明。
  - 保留 `目标 xx 秒建议图片数量`。
  - 保留 `当前本地图片数量`。
- 保持不变：
  - 底层整数秒片段分配。
  - `video_clip_durations` 计算和参数写入。
  - 图片数量校验和生成前拦截。
  - 视频生成流程。
  - `app/services/video.py`。
  - `app/services/task.py`。
  - `app/models/schema.py`。

## WebUI API Key 管理入口隐藏

- 本次目标：
  - 当前餐厅 MVP 使用本地上传图片，普通用户界面不再展示 Pexels / Pixabay API Key 管理。
- 调整内容：
  - 隐藏右侧 `API Key 管理` 入口。
  - 隐藏 Pexels / Pixabay API Key 增删控件。
  - 保留底层 API Key 管理代码和配置。
- 保持不变：
  - 未删除已有 API Key。
  - 未修改 `config.toml`。
  - 本地图片上传。
  - `AI生成视频文案` 按钮。
  - 视频生成核心。

## WebUI 主页面两列布局

- 本次目标：
  - 隐藏 API Key 管理后，移除右侧空白列。
  - 让文案设置和视频设置两列填满页面宽度。
- 调整内容：
  - 主页面由三列改为两列。
  - 左列保留文案设置。
  - 右列承载视频设置、音频设置、字幕设置。
  - 右列顺序保持为 `视频设置` → `音频设置` → `字幕设置`。
  - 不再创建或显示第三个右侧空白列。
- 保持不变：
  - 本地图片上传。
  - 目标时长。
  - 图片数量校验。
  - 底层整数秒片段分配。
  - 文案字数校验。
  - `AI生成视频文案` 按钮。
  - 字幕生成、音频生成、视频生成核心。

## 第 2 阶段 restaurant_engine Pipeline 骨架

- 本次目标：
  - 创建 `restaurant_engine` 最小 Pipeline 骨架。
  - 从仓库外样本读取 `project.json`。
  - 复用已有 validator。
  - 扫描本地图片目录。
  - 创建样本项目 `output/`。
  - 输出 mock `storyboard.json` 和 `pipeline_report.json`。
- 新增/调整内容：
  - 新增 pipeline 数据结构。
  - 新增 `restaurant_engine/pipeline.py`。
  - 新增 `restaurant_engine/pipeline_project.py` CLI。
  - 新增 `restaurant_docs/PIPELINE_SPEC.md`。
- 当前明确不做：
  - 不生成视频。
  - 不调用 DeepSeek。
  - 不调用 TTS。
  - 不调用 AI 图生视频。
  - 不调用外部 API。
  - 不修改 WebUI。
  - 不修改 MoneyPrinterTurbo 原有业务代码。
  - 不修改视频生成核心。
- 验证样本：
  - `/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/project.json`
- 预期输出：
  - `/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/output/storyboard.json`
  - `/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/output/pipeline_report.json`

## 第 2 阶段 DeepSeek planner 安全接入

- 本次目标：
  - 在 `restaurant_engine` 中新增 DeepSeek planner 能力。
  - pipeline 支持 `mock` 和 `deepseek` planner。
  - 默认 planner 必须保持 `mock`。
  - DeepSeek 调用必须由用户显式开启。
- 调整内容：
  - 新增 `restaurant_engine/deepseek_client.py`。
  - 新增 `restaurant_engine/storyboard_planner.py`。
  - `run_pipeline(...)` 增加 `planner` 和 `allow_external_api` 参数。
  - CLI 增加 `--planner mock|deepseek` 和 `--allow-external-api`。
  - `PipelineReport` 增加 `planner`、`external_api_allowed`、`external_api_called`。
  - `.gitignore` 补充常见敏感文件规则。
- 安全约束：
  - 默认 mock 模式不读取 DeepSeek key，不调用外部 API。
  - `--planner deepseek` 未带 `--allow-external-api` 时阻止运行。
  - report 不写 API Key、请求头、完整 prompt/response。
- 保持不变：
  - 未修改 WebUI。
  - 未修改 `app/services/llm.py`。
  - 未修改视频生成核心。
  - 本轮验证不主动调用 DeepSeek 或任何外部 API。

## DeepSeek planner 真实调用测试记录

- 输入 `project.json`：
  - `/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/project.json`
- 执行命令：
  - `python3 -m restaurant_engine.pipeline_project --project /Users/feei/AI/restaurant-video-ai-samples/sichuan_001/project.json --planner deepseek --allow-external-api`
- 输出文件：
  - `/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/output/storyboard.json`
  - `/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/output/pipeline_report.json`
- 测试结果：
  - `ok=true`
  - `planner=deepseek`
  - `external_api_allowed=true`
  - `external_api_called=true`
  - `validation_passed=true`
  - `image_count=8`
  - `scene_count=8`
  - scene 顺序正确。
  - storyboard 包含真实中文餐厅宣传旁白摘要。
- 安全检查：
  - 未发现 `sk-` / `api_key` / `Authorization` / `Bearer` 写入 report 或 storyboard。
  - 仓库内未误生成 report/storyboard。
  - 未生成视频。
  - 未修改代码。
- 非阻塞问题：
  - DeepSeek 返回 `total duration field` 为 `24`，8 个 scene 每个 3 秒。
  - 后续需要增强 `target_duration_seconds` 时长约束，或由后续时长分配模块覆盖。
- 结论：
  - DeepSeek planner 真实调用已打通。

## DeepSeek planner 时长约束增强

- 本次目标：
  - 修复 DeepSeek planner 返回 scene duration 与目标时长不一致的问题。
  - 将 mock planner 和 DeepSeek planner 统一到本地整数秒 duration 分配逻辑。
- 调整内容：
  - 新增 `compute_scene_durations(target_duration_seconds, image_count)`。
  - `project.json` 缺少 `target_duration_seconds` 时沿用默认 `30` 秒。
  - mock storyboard 使用本地 duration 分配，不再固定每张图 `5` 秒。
  - DeepSeek prompt 写入目标时长、图片数量和必需 scene duration 列表。
  - DeepSeek 返回后，本地覆盖所有 scene 的 `duration_seconds`。
  - `Storyboard` 增加标准 `total_duration_seconds`。
  - `PipelineReport` 增加 `target_duration_seconds`、`scene_count`、`scene_durations`、`total_duration_seconds`、`duration_normalized`。
- 关键验证目标：
  - `30 秒 / 8 图` 应输出 `4, 4, 3, 4, 4, 3, 4, 4`。
  - mock pipeline 的 `total_duration_seconds` 应为 `30`。
  - DeepSeek 未授权时仍不调用外部 API。
- 安全边界：
  - 本轮不调用 DeepSeek。
  - 本轮不调用任何外部 API。
  - 本轮不生成视频。
  - 未修改 WebUI。
  - 未修改 `app/`。
  - 未修改 `config.toml`。
  - 未修改 MoneyPrinterTurbo 视频生成核心。

## DeepSeek planner 时长对齐真实测试记录

- 输入 `project.json`：
  - `/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/project.json`
- 执行命令：
  - `python3 -m restaurant_engine.pipeline_project --project /Users/feei/AI/restaurant-video-ai-samples/sichuan_001/project.json --planner deepseek --allow-external-api`
- 执行环境说明：
  - 系统 `python3` 缺少项目依赖。
  - 本次实际使用项目 `.venv` Python 执行同等 pipeline 命令。
- 输出文件：
  - `/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/output/storyboard.json`
  - `/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/output/pipeline_report.json`
- 测试结果：
  - `ok=true`
  - `planner=deepseek`
  - `external_api_allowed=true`
  - `external_api_called=true`
  - `target_duration_seconds=30`
  - `scene_durations=[4, 4, 3, 4, 4, 3, 4, 4]`
  - `storyboard total_duration_seconds=30`
  - `duration_sum=30`
  - `image_count=8`
  - `scene_count=8`
  - scene 顺序正确。
  - storyboard 含真实中文餐厅宣传文案摘要，例如“正宗川味太上头，麻辣鲜香，一吃就停不下来！”。
  - 未出现 mock 占位文案；兼容字段保留，但内容为真实文案。
- 安全检查：
  - 未发现 `sk-` / `api_key` / `Authorization` / `Bearer` 写入 report 或 storyboard。
  - 仓库内未误生成 report/storyboard。
  - 未生成视频。
  - 未修改代码。
- 阻塞问题：
  - 无。
- 非阻塞问题：
  - 系统 `python3` 缺少项目依赖，本次实际使用项目 `.venv` Python 执行。
- 结论：
  - DeepSeek planner 真实调用 + 时长对齐已通过。
  - 真实 DeepSeek 返回后，scene duration 已被本地强制归一化到 `target_duration_seconds=30`。

## Storyboard contract 强化

- 本次目标：
  - 在进入 TTS、图生视频和视频合成前，为 `storyboard.json` 增加结构门禁。
  - pipeline 生成 storyboard 后自动校验结构、时长、图片顺序和字段完整性。
- 新增/调整内容：
  - 新增 `restaurant_engine/storyboard_contract.py`。
  - 新增 `StoryboardContractIssue`。
  - 新增 `StoryboardContractReport`。
  - 新增 `validate_storyboard_contract(...)`。
  - 新增 `storyboard_contract_report_to_dict(...)`。
  - pipeline 新增 `validate_storyboard_contract` step。
  - `PipelineReport` 增加：
    - `storyboard_contract_passed`
    - `storyboard_contract_errors`
    - `storyboard_contract_warnings`
    - `duration_sum`
  - CLI 摘要增加 storyboard contract 状态、duration sum、errors count、warnings count。
- 校验规则摘要：
  - scene 数量等于图片数量。
  - scene 顺序等于图片文件名排序。
  - scene 必填字段完整。
  - `index` 从 `1` 开始连续递增。
  - `duration_seconds` 为正整数。
  - duration 总和等于 `target_duration_seconds`。
  - `storyboard.total_duration_seconds` 与目标时长对齐。
  - narration 不为空。
  - mock planner 中 mock 占位文案记 warning。
  - DeepSeek planner 中 mock 占位文案记 error。
- 当前边界：
  - 本轮不调用 DeepSeek。
  - 本轮不调用任何外部 API。
  - 本轮不生成视频。
  - 未修改 WebUI。
  - 未修改 `app/`。
  - 未修改 `config.toml`。
  - 未修改视频生成核心。

## Storyboard quality contract 增强

- 本次目标：
  - 在结构 contract 之后增加内容质量门禁。
  - 确保 storyboard 在进入 TTS、图生视频和视频合成前具备基本宣传片可用性。
- 新增/调整内容：
  - `StoryboardScene` 增加：
    - `visual_instruction`
    - `selling_point`
    - `transition_hint`
  - 新增 `StoryboardQualityReport`。
  - 新增 `validate_storyboard_quality_contract(...)`。
  - 新增 `storyboard_quality_report_to_dict(...)`。
  - pipeline 新增 `validate_storyboard_quality` step。
  - `PipelineReport` 增加：
    - `storyboard_quality_passed`
    - `storyboard_quality_errors`
    - `storyboard_quality_warnings`
  - CLI 摘要增加 storyboard quality 状态、quality errors count、quality warnings count。
  - mock planner 改为输出中文餐厅宣传文案，不再输出简单英文 mock 文案。
  - mock planner 输出完整质量字段。
  - DeepSeek prompt 要求返回完整质量字段。
  - DeepSeek 返回后保留质量字段。
- quality contract 规则摘要：
  - narration 非空。
  - narration 包含中文。
  - narration 中文字符数不应过短或过长。
  - scene narration 不重复。
  - `visual_instruction`、`selling_point`、`transition_hint` 非空。
  - 不允许明显 mock / placeholder 文案。
  - DeepSeek planner 不允许 mock / placeholder 文案。
- 当前边界：
  - 本轮不调用 DeepSeek。
  - 本轮不调用任何外部 API。
  - 本轮不生成视频。
  - 未修改 WebUI。
  - 未修改 `app/`。
  - 未修改 `config.toml`。
  - 未修改视频生成核心。

## Storyboard quality contract 阈值修正

- 背景：
  - 真实 DeepSeek planner quality contract 测试中，scene 1 返回“正宗川味，太上头！”。
  - 该文案是可用于餐厅宣传片的中文短句，但中文字符数为 7。
  - 原规则把少于 8 个中文字符的 narration 直接判为 `narration_too_short` error，导致 quality contract 失败。
- 本轮修正：
  - 空 narration 仍为 error。
  - 非中文 narration 仍为 error，错误码为 `non_chinese_narration`。
  - 少于 4 个中文字符的极短 narration 仍为 hard error，错误码为 `narration_too_short_hard`。
  - 4 到 7 个中文字符的 narration 降级为 warning，错误码仍为 `narration_too_short`。
  - DeepSeek prompt 增强：要求自然中文短句，优先不少于 8 个中文字符，不返回过短片段、mock、placeholder、TODO、待填写或 Markdown。
- 保留规则：
  - 缺少 `visual_instruction`、`selling_point`、`transition_hint` 仍为 error。
  - duplicate narration 仍为 error。
  - DeepSeek planner 中 mock / placeholder 文案仍为 error。
- 本轮验证目标：
  - 默认 mock pipeline 仍通过 structure contract 和 quality contract。
  - 本地 fake DeepSeek storyboard 中“正宗川味，太上头！”应通过 quality contract。
  - DeepSeek 未授权调用仍应被阻止，且不调用外部 API。
- 当前边界：
  - 本轮不调用 DeepSeek。
  - 本轮不调用任何外部 API。
  - 本轮不生成视频。
  - 未修改 WebUI、`app/`、`config.toml` 或视频生成核心。

## DeepSeek storyboard quality contract 真实复测记录

- 输入 project.json：
  - `/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/project.json`
- 执行命令：
  - `.venv/bin/python -m restaurant_engine.pipeline_project --project /Users/feei/AI/restaurant-video-ai-samples/sichuan_001/project.json --planner deepseek --allow-external-api`
- 输出文件：
  - `/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/output/storyboard.json`
  - `/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/output/pipeline_report.json`
- 测试结果：
  - `ok=true`
  - `planner=deepseek`
  - `external_api_allowed=true`
  - `external_api_called=true`
  - `storyboard_contract_passed=true`
  - `storyboard_quality_passed=true`
  - `quality_errors=0`
  - `quality_warnings=3`
  - `target_duration_seconds=30`
  - `scene_durations=[4,4,3,4,4,3,4,4]`
  - `duration_sum=30`
  - `image_count=8`
  - `scene_count=8`
  - scene 顺序正确。
  - `narration` / `visual_instruction` / `selling_point` / `transition_hint` 均存在。
- 安全检查：
  - 未发现 `sk-` / `api_key` / `Authorization` / `Bearer` 写入 report 或 storyboard。
  - 仓库内未误生成 report/storyboard。
  - 未生成视频。
  - 未修改代码。
- 结论：
  - DeepSeek storyboard quality contract 真实复测通过。

## TTS contract / narration plan 骨架

- 本次目标：
  - 在接入真实 TTS 前，从 storyboard 生成 `narration_plan.json`。
  - 校验每个 scene 的 narration 是否大致适合对应 `duration_seconds`。
- 新增/调整内容：
  - 新增 `NarrationLine`。
  - 新增 `NarrationPlan`。
  - 新增 `TTSContractReport`。
  - 新增 `restaurant_engine/narration_plan.py`。
  - pipeline 新增 `build_narration_plan` step。
  - pipeline 新增 `validate_tts_contract` step。
  - pipeline 新增 `write_narration_plan` step。
  - `pipeline_report.json` 新增：
    - `narration_plan_path`
    - `tts_contract_passed`
    - `tts_contract_errors`
    - `tts_contract_warnings`
    - `narration_line_count`
    - `total_estimated_speech_seconds`
  - CLI 摘要增加 TTS contract 状态、errors/warnings 数量和 narration plan 路径。
- 当前校验规则：
  - narration 为空：error。
  - narration 不含中文：error。
  - scene duration 非正数：error。
  - 估算朗读时长超过 scene duration：warning。
  - 估算朗读时长明显超过 scene duration：error。
- 当前边界：
  - 本轮不调用 DeepSeek。
  - 本轮不调用任何外部 API。
  - 本轮不调用 TTS。
  - 本轮不生成音频。
  - 本轮不生成视频。
  - 未修改 WebUI、`app/`、`config.toml` 或视频生成核心。

## DeepSeek narration plan / TTS contract 真实复测记录

- 输入 project.json：
  - `/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/project.json`
- 执行命令：
  - `.venv/bin/python -m restaurant_engine.pipeline_project --project /Users/feei/AI/restaurant-video-ai-samples/sichuan_001/project.json --planner deepseek --allow-external-api`
- 输出文件：
  - `/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/output/storyboard.json`
  - `/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/output/pipeline_report.json`
  - `/Users/feei/AI/restaurant-video-ai-samples/sichuan_001/output/narration_plan.json`
- 测试结果：
  - `ok=true`
  - `planner=deepseek`
  - `external_api_allowed=true`
  - `external_api_called=true`
  - `storyboard_contract_passed=true`
  - `storyboard_quality_passed=true`
  - `tts_contract_passed=true`
  - `storyboard_quality_errors=0`
  - `tts_contract_errors=0`
  - `storyboard_quality_warnings=4`
  - `tts_contract_warnings=5`
  - `target_duration_seconds=30`
  - `scene_durations=[4,4,3,4,4,3,4,4]`
  - `duration_sum=30`
  - `narration_line_count=8`
  - `estimated_total_tts_seconds=32.0`
  - `total_cjk_chars=128`
  - `image_count=8`
  - `scene_count=8`
  - scene 顺序正确。
  - narration line 顺序正确。
- 安全检查：
  - 未发现 `sk-` / `api_key` / `Authorization` / `Bearer` 写入输出文件。
  - 仓库内未误生成 report/storyboard/narration_plan。
  - 未生成音频。
  - 未生成视频。
  - 未修改代码。
- 非阻塞问题：
  - 系统 `python3` 缺少项目依赖，使用 `.venv/bin/python` 执行。
  - TTS warning 为估算时长提醒，不阻断 pipeline。
  - 估算朗读总时长为 32.0 秒，后续真实 TTS 阶段需校准。
- 结论：
  - DeepSeek narration plan / TTS contract 真实复测通过。

## Mock Image Understanding 骨架

- 本次目标：
  - 在接入真实图片理解、OCR、图生视频和封面筛选前，先生成本地 mock `image_understanding.json`。
  - 将图片理解结果写入 `pipeline_report.json`，作为后续链路前置 contract。
- 新增/调整内容：
  - 新增 `ImageUnderstandingItem`。
  - 新增 `ImageUnderstandingReport`。
  - 新增 `restaurant_engine/image_understanding.py`。
  - pipeline 新增 `build_image_understanding` step。
  - pipeline 新增 `write_image_understanding` step。
  - `pipeline_report.json` 新增：
    - `image_understanding_path`
    - `image_understanding_passed`
    - `allowed_image_count`
    - `rejected_image_count`
    - `image_category_counts`
  - CLI 摘要增加图片理解状态、allowed/rejected 数量、分类统计和输出路径。
  - 新增 `restaurant_docs/IMAGE_UNDERSTANDING_SPEC.md` 记录字段和规则。
- 当前规则：
  - 只基于文件名识别图片类型。
  - `intro` / `interior` / `dish` / `dining` / `detail` / `extra` / `logo` / `other` 为可用或待复核类型。
  - 包含 `qrcode` / `qr` / `phone` / `tel` / `address` / `menu` / `price` / `contact` / `wechat` / `wx` 的文件名标记为 `invalid_*`。
  - rejected images 当前只产生 warning，不阻断 pipeline。
  - 没有图片时产生 error，pipeline `ok=false`。
- 当前边界：
  - 本轮不调用 DeepSeek。
  - 本轮不调用任何外部 API。
  - 本轮不调用 TTS。
  - 本轮不调用视觉模型或 OCR。
  - 本轮不生成音频。
  - 本轮不生成视频。
  - 未修改 WebUI、`app/`、`config.toml` 或视频生成核心。

## 图片理解 Provider 架构调整

- 背景：
  - 用户确认手机上传图片文件名通常没有语义。
  - 文件名规则不能作为正式产品图片理解主逻辑。
- 本次目标：
  - 暂停“根据文件名规则识别图片类别”作为主逻辑。
  - 将文件名规则降级为显式 fallback。
  - 建立 image understanding provider 架构。
- 新增/调整内容：
  - `mock` provider：默认模式，只生成开发占位，不读取图片内容，也不使用文件名语义。
  - `filename_fallback` provider：保留原文件名规则，仅用于开发测试或无视觉模型时兜底。
  - `vision` provider：未来真实图片内容理解入口，当前占位未实现。
  - CLI 新增 `--image-understanding-provider`。
  - `pipeline_report.json` 新增 `image_understanding_provider`。
  - `image_understanding.json` 顶层新增 `provider`，单图新增 `source`。
  - 新增 `restaurant_docs/IMAGE_UNDERSTANDING_PROVIDER_SPEC.md`。
- 安全边界：
  - 默认不调用外部 API。
  - `vision` provider 必须显式 `--image-understanding-provider vision --allow-external-api`。
  - 当前 `vision` provider 尚未实现，不会调用外部 API。
  - 本轮不调用 DeepSeek、不调用 TTS、不调用视觉模型、不生成音频、不生成视频。
  - 未修改 WebUI、`app/`、`config.toml` 或视频生成核心。

## 本地规则引擎骨架

- 本次目标：
  - 在 `image_understanding.json` 之后、`storyboard.json` 之前新增本地 rule engine。
  - 输出 `rule_engine_report.json`。
  - 将 rule engine 摘要写入 `pipeline_report.json`。
- 新增/调整内容：
  - 新增 `restaurant_engine/rule_engine.py`。
  - 新增 rule engine 相关模型：
    - `RuleFinding`
    - `RuleEngineSummary`
    - `RuleAssetGroups`
    - `StoryboardHints`
    - `RuleEngineReport`
  - pipeline 新增 `build_rule_engine_report` step。
  - pipeline 新增 `write_rule_engine_report` step。
  - CLI 摘要新增 rule engine 状态。
  - 新增 `restaurant_docs/RULE_ENGINE_SPEC.md`。
- 当前 contract：
  - `engine=local_static`
  - `external_api_called=false`
  - `blocking=false`
  - 只消费 `image_understanding`。
  - 不重新读取文件名。
  - 不读取图片像素内容。
  - 不调用任何外部 API。
- 当前 findings：
  - `NO_CONTENT_BASED_UNDERSTANDING`：mock provider，仅开发占位。
  - `FILENAME_FALLBACK_USED`：filename fallback provider，仅开发兜底。
  - `UNKNOWN_IMAGE_UNDERSTANDING_PROVIDER`：未知 provider，需要人工复核。
- 当前输出：
  - `summary.image_count`
  - `summary.category_counts`
  - `summary.has_content_based_understanding`
  - `summary.has_filename_fallback`
  - `asset_groups.hero_candidates`
  - `asset_groups.dish_candidates`
  - `asset_groups.interior_candidates`
  - `asset_groups.fallback_candidates`
  - `storyboard_hints.preferred_opening_image_id`
  - `storyboard_hints.avoid_repeating_same_image`
  - `storyboard_hints.requires_human_review`
- 当前边界：
  - 未调用 DeepSeek。
  - 未调用任何外部 API。
  - 未调用 TTS。
  - 未生成音频。
  - 未生成视频。
  - 未修改 WebUI、`app/`、`config.toml` 或视频生成核心。
