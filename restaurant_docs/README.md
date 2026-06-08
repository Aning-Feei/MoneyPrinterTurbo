# 餐饮 AI 宣传视频生成系统 - 原型验证

本目录用于记录餐饮 AI 宣传视频生成系统的原型验证过程。

当前阶段目标：
- 基于 MoneyPrinterTurbo 做第一阶段生成能力验证。
- MoneyPrinterTurbo 仅作为生成引擎验证仓库。
- 不把 MoneyPrinterTurbo WebUI 作为最终正式产品。
- 后续会新建 restaurant-video-ai 作为正式产品项目。
- 当前阶段优先验证：本地图片、封面、分镜、AI 图生视频、口播、字幕、BGM、最终视频合成。

开发约束：
- 不覆盖 config.toml。
- 不提交 API Key。
- 不提交 webui.log 和 webui.pid。
- 不直接大规模重构 MoneyPrinterTurbo 原始代码。
- 新功能优先放在 restaurant_engine/ 中验证。
