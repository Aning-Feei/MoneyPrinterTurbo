# TwinkleBite AI 本地运行与测试说明

## 1. 当前分支和远程

- 当前开发分支：`feature/restaurant-video-prototype`
- 远程 fork：`origin = https://github.com/Aning-Feei/MoneyPrinterTurbo.git`
- 原始上游：`upstream = https://github.com/harry0703/MoneyPrinterTurbo.git`

## 2. 启动 WebUI

### 2.1 前台启动

```bash
cd /Users/feei/AI/MoneyPrinterTurbo
sh ./webui.sh
```

- 默认地址：`http://127.0.0.1:8501`
- 如果 WebUI 是前台运行，终端不要关闭。
- 如果关闭终端，WebUI 可能停止。

### 2.2 后台启动、状态和停止

```bash
cd /Users/feei/AI/MoneyPrinterTurbo
scripts/twinkle_webui_start.sh
scripts/twinkle_webui_status.sh
scripts/twinkle_webui_stop.sh
```

- 后台启动会写入 `.runtime/twinkle_webui.pid`。
- 日志写入 `.runtime/twinkle_webui.log`。
- `.runtime/` 不进入 Git。
- 如果端口 8501 已被前台 WebUI 占用，`twinkle_webui_start.sh` 会拒绝启动，不会强杀进程。
- 如果用户正在前台运行 `sh ./webui.sh`，应先在那个终端按 `Ctrl+C` 停止，再使用后台脚本。
- 用户已在本机 macOS 手动验证：start 成功，关闭终端后 WebUI 仍保持运行，status 可看到 PID 运行和 8501 监听，stop 成功，stop 后 PID 文件不存在且 8501 无 listener。

## 3. 基本测试流程

1. 打开 WebUI：`http://127.0.0.1:8501`
2. 设置目标视频时长：30 / 40 / 50 / 60 秒。
3. 上传本地餐厅图片。
4. 检查页面显示：
   - 每张图片展示时长
   - 预计图片总覆盖时长
   - 图片数量是否符合推荐范围
   - 文案字数是否符合目标时长范围
5. 输入视频文案。
6. 点击生成视频。
7. 查看 `final-*.mp4`。
8. 人工检查图片、字幕、语音、BGM。

## 4. 已验证测试矩阵

| Case | 目标时长 | 图片数量 | 片段分配 | 结果 |
|---|---:|---:|---|---|
| A | 30 秒 | 8 张 | 4,4,3,4,4,3,4,4 | 通过 |
| B | 30 秒 | 6 张 | 5,5,5,5,5,5 | 通过 |
| C | 40 秒 | 8 张 | 5,5,5,5,5,5,5,5 | 通过 |
| D | 50 秒 | 10 张 | 5,5,5,5,5,5,5,5,5,5 | 通过，暂未发现问题 |
| E | 60 秒 | 12 张 | 5,5,5,5,5,5,5,5,5,5,5,5 | 通过，暂未发现问题 |

## 5. Git 常用命令

```bash
git status --short
git branch -vv
git log --oneline -8
git push
```

## 6. 注意事项

- 不要提交 `storage/`。
- 不要提交生成视频。
- 不要提交 `.pyc` / `__pycache__`。
- 不要把 API Key、GitHub token、密码写入文档或提交。
- 测试 `AI生成视频文案` 按钮会调用外部 API，只有用户明确要测试时才点击。
