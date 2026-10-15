# 任务清单

## 阶段一：规划

- [x] 检查目录与已有文件，确认目标目录不存在
- [x] 确定六模块边界、受众、技术栈、目录、依赖与版本决策
- [x] 输出 PROJECT_PLAN.md

## 阶段二：MVP

- [x] 可安装 Python 包、CLI、中文 README 与英文入口
- [x] Caesar 加解密、频率分析与离线交互图
- [x] AES-GCM 往返与认证失败示例
- [x] 三种 KDF、随机盐、验证及有界进程基准
- [x] pytest、Ruff、CI、贡献、安全政策、MIT 许可
- [x] Issue/PR 模板、依赖更新配置
- [x] 12 周路线、15 个后续主题、单篇文章稿

## 首次提交验证

- [x] 依赖安装、pip check、精确锁文件
- [x] 最终 pytest、Ruff、三个演示、README 代码及链接检查
- [x] wheel/sdist 构建与干净环境 wheel 运行
- [x] 常见敏感信息模式及人工审查
- [x] main 初始化、用户署名、本地首次 Commit

## 后续（需维护者操作或后续任务）

- [x] 用户创建 GitHub 仓库、设置远程并完成首次 push
- [x] 首次远程 CI 已实际执行并读取结果
- [ ] 启用私密漏洞报告与 Discussions
- [ ] 配置实际 Topics、标签与 Good First Issues
- [ ] 确认后发布今天仅一篇文章
- [ ] 按路线实现 Vigenère、仿射密码及更多主题

## 首次远程 CI 修复

- [x] 读取首次提交和 Dependabot 分支 CI 日志，确认 Windows 的两个 CLI 测试失败
- [x] 将测试入口路径改为 sysconfig scripts 路径，保留实际 CLI 子进程调用
- [x] 本地重新运行测试、Ruff 和文档检查
- [ ] 用户推送修复后，核实六项远程 CI 的新结果
