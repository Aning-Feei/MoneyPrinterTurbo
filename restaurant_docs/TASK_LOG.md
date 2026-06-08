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
