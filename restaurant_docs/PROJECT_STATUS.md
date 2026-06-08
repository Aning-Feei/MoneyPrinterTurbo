# 项目状态

## 项目基本信息

- 项目名称：餐饮 AI 宣传视频生成系统
- 当前仓库：/Users/feei/AI/MoneyPrinterTurbo
- 当前分支：feature/restaurant-video-prototype
- 当前阶段：第 1 阶段：MoneyPrinterTurbo 基础生成链路验证（进行中）
- 当前下一步：只读分析图片输入顺序、脚本片段顺序、local_videos 生成顺序、最终合成顺序之间的关系

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

## 当前阻塞点

无

## 下一步目标

只读分析图片输入顺序、脚本片段顺序、local_videos 生成顺序、最终合成顺序之间的关系；暂不修改业务代码。

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
