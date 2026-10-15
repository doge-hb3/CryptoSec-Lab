# 贡献指南

欢迎可复现错误报告、文档改进和有教学价值的实验。先阅读 README 和对应模块指南，再选择任务。小改动可直接提交 PR；新算法先讨论教学目标、威胁模型与验收条件。

## 本地验证

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
python -m ruff check .
python -m ruff format --check .
python scripts/check_repository.py
python -m build
```

以上 `python` 指已安装项目的虚拟环境解释器。Windows 可用 `.venv\Scripts\python.exe`。新增实验至少包含已知向量或独立库互操作、异常路径、运行指令与真实结果。不能只测试实现复制品。改 README 命令时同步执行。

每个专题提供理论、Python 入口、实验结果、误区、安全建议与一手来源。所有口令数据程序生成；不接收泄露数据集、真实凭据、远程账户测试或认证绕过功能。不要提交密钥、环境变量文件、绝对本机路径或用户名。提交前检查 `git diff --cached`。

## 审查与发布

PR 描述问题、改变行为、运行命令与结果。CI 通过后仍需维护者审查。依赖更新同时更新范围及锁文件，校验 Python/OS 矩阵，检查发布说明。未经维护者确认，不自动创建远程仓库、push 或发布 Release。

建议首批任务见 [COMMUNITY.md](docs/COMMUNITY.md)。文档可用 `documentation`；明确小任务可用 `good first issue`。这些标签需要仓库创建后手工配置，不能假定已存在。
