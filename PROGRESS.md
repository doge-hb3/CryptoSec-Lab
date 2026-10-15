# 实施进度

日期：2026-10-15。最终目录为用户指定的 `D:\GitHub\CryptoSec-Lab`；创建前不存在。未删除已有文档或其他项目；早期工作目录的初稿保留。

## 阶段一已完成

创建 PROJECT_PLAN.md、TASKS.md，记录技术选择、六模块范围、版本和资源边界。检查命令：Get-ChildItem、Test-Path、父级 AGENTS.md 检查。未发现适用的额外 AGENTS.md。

## 阶段二已完成

创建 src 包及三个实验、CLI、基准子进程、pytest 测试、中英文入口、主题指南、GitHub 配置、许可、安全与贡献规范、离线可视化、12 周路线和一篇文章稿。实际文件清单见 FILES.md。

## 验证过程

首次在 README 尚未生成时执行 `pip install -e '.[dev]'`，构建元数据失败，原因是 README.md 缺失。补齐后使用官方 PyPI 重试成功；不是依赖或算法运行失败。

首轮 pytest：52 passed。首轮 Ruff 发现导入顺序与长行，已调整。复核中发现频率分析可能把非 ASCII 字符的大写展开计入英语统计，已改为先过滤 ASCII 并增加回归测试。CLI 测试已改用当前解释器旁的入口，避免依赖环境激活。

Windows 虚拟环境启动器使首次 RSS 采样约 4 MiB，复核后改为采样整个子进程树并重跑，实际记录保存在 docs/results/benchmark.json。严格锁定构建环境时首次缺少 hatchling 的 editable 后端依赖 editables，已将其显式加入开发依赖和精确锁文件；使用锁文件和 --no-build-isolation 重装成功。

最终执行（所有命令使用本项目 .venv 的解释器或入口）：

| 命令 | 实际结果 |
| --- | --- |
| python -m pip install -e '.[dev]' | 安装成功 |
| python -m pip install -r requirements-dev.lock | 精确依赖全部满足 |
| python -m pip install --no-deps --no-build-isolation -e . | 成功，验证 CI 安装路径 |
| python -m pip check | No broken requirements found |
| python -m pytest -q | 53 passed，最终记录 4.91s |
| python -m ruff check . | All checks passed |
| python -m ruff format --check . | 通过 |
| python scripts/check_repository.py | 本地文档链接、所有 Python 文档例子、常见密钥/Token 模式通过 |
| cryptosec caesar | 往返和频率样例恢复均 true，shift=7 |
| cryptosec aes | 往返和篡改拒绝均 true，nonce=12 字节 |
| cryptosec kdf --repeats 3 | 三种算法均完成 3 轮，原始时间/内存样本已保存 |
| python -m build --no-isolation | wheel 与 sdist 构建成功 |

命令原始输出见 docs/results/verification.txt。另外在独立的 `.venv/wheel-smoke` 环境安装实际 wheel，依次执行 caesar、aes、kdf --repeats 1，均成功；确认导入路径位于该环境 site-packages，未使用 editable 源码。

源码人工检查：没有硬编码真实密钥、Token 或真实用户口令；密钥、盐和实验口令均动态生成。已知向量为公开教学字符串，基准文件只记录参数和资源数据。模式检查不能证明不存在任何漏洞，不将其表述为完整安全审计。

Git 已初始化为 main，使用用户提供的署名并只设置于本仓库。首次提交信息为 `feat: bootstrap CryptoSec-Lab teaching MVP`，实际提交哈希以 `git log -1` 及最终汇报为准。没有配置 remote，也没有创建公开仓库、远程 Release 或 push。CI 的其他系统/解释器版本尚待远程执行。今天只有一篇文章稿，按最新约束保留本地待发布。
