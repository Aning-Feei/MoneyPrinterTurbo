# 餐饮 AI 宣传视频生成系统 - 项目计划

项目当前阶段：MoneyPrinterTurbo 生成能力验证。

## 第一个最小闭环目标

用户准备 6 张餐饮图片和一个 project.json，restaurant_engine 读取这些输入，输出：
- image_understanding.json
- cover.jpg
- storyboard.json
- clips/
- final/final_video.mp4

第一版允许先使用 Mock AI 图生视频 Provider，不直接调用真实 AI 图生视频服务。

第一版 restaurant_engine 不直接改 MoneyPrinterTurbo WebUI，不处理用户系统，不处理支付，不处理电话/地址/二维码。

## 图片最低要求

- 至少 6 张，最多 12 张
- 门头或招牌菜引入至少 1 张
- 店内环境至少 1 张
- 招牌菜至少 2 张
- 顾客就餐或聚餐氛围至少 1 张

## 视频规则

- 封面只展示主标题
- 封面作为第一帧并停留约 1 秒
- 每张合格图片生成一个视频片段
- 每段视频 3～5 秒，最长不超过 5 秒
- 默认开启 AI 旁白式口播
- 不展示电话、地址、二维码、菜单价格
