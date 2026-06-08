# Codex 执行控制规范

## 1. 目录门禁

每次 Codex 执行任务前必须先确认：

- pwd 必须是 /Users/feei/AI/MoneyPrinterTurbo
- 当前 git 分支必须是 feature/restaurant-video-prototype

如果任一条件不满足，必须立即停止，不得读取、创建或修改任何文件。

## 2. 总原则

Codex 每次只能执行当前任务明确授权的内容。

没有明确授权，不得：
- 创建额外文件
- 修改额外文件
- 删除文件
- 大范围重构
- 扫描整个项目
- 读取无关代码
- 调用外部 API
- 修改配置文件
- 打印 API Key
- 提交 Git commit

## 3. 每次任务必须包含

每次给 Codex 的任务必须包含：

1. 当前阶段
2. 本次目标
3. 目录门禁
4. 允许修改的文件
5. 禁止修改的文件
6. 禁止执行的行为
7. 允许读取的文件
8. 精确执行步骤
9. 测试命令
10. 完成后汇报格式

如果任务缺少这些信息，Codex 应先请求补充，而不是自行推断。

## 4. 默认禁止修改文件

除非任务明确允许，否则禁止修改：

- config.toml
- config.example.toml
- pyproject.toml
- uv.lock
- requirements.txt
- docker-compose.yml
- Dockerfile
- webui/Main.py
- app/services/*
- app/models/*
- app/config/*
- resource/*
- .env
- 任何包含 API Key 的文件

## 5. 默认禁止行为

除非任务明确允许，否则禁止：

- 使用 sudo
- rm -rf
- chmod -R 777
- pip install --break-system-packages
- 修改依赖
- 修改锁文件
- 访问外部 API
- 上传文件到外部服务
- 打印环境变量
- 打印 API Key
- 执行全项目格式化
- 执行全项目重构
- 提交 git commit
- 删除样本图片
- 复制样本图片进仓库

## 6. 文件读取规则

Codex 只能读取当前任务所需文件。

默认禁止：
- 全项目搜索
- 大范围 find
- 大范围 grep
- 无目标阅读 app/services、webui、app/models

如果确实需要搜索，必须先说明：
- 为什么需要搜索
- 搜索范围
- 搜索关键词
- 预期结果

并等待确认后再执行。

## 7. 输出控制

Codex 每次任务完成后必须汇报：

1. 当前 pwd
2. 当前分支
3. 实际读取了哪些文件
4. 实际修改了哪些文件
5. 实际新增了哪些文件
6. 是否修改了禁止文件
7. 是否调用了外部 API
8. 是否执行了依赖安装
9. 测试命令和测试结果
10. 输出文件路径
11. 是否存在未完成事项
12. 下一步建议

## 8. Git 控制

Codex 可以执行：

- git status
- git diff -- 文件名
- git branch --show-current

Codex 不得执行：

- git add
- git commit
- git push
- git reset
- git clean
- git checkout main
- git merge
- git rebase

除非用户明确授权。

## 9. 当前项目安全边界

当前阶段，MoneyPrinterTurbo 仅作为生成能力验证仓库。

新增功能优先放在：

- restaurant_engine/
- restaurant_docs/

不要直接改 MoneyPrinterTurbo 原有业务流程。
