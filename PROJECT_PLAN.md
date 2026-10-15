# CryptoSec-Lab 项目规划

决策日期：2026-10-15。当前范围：阶段一规划、阶段二 MVP；为首次本地提交执行必要的阶段三验证。阶段四、五提供基础配置与后续计划，不宣称已形成社区。

## 用户与价值

初学者通过可运行的例子区分编码、加密、哈希和认证；有基础的安全人员可检查威胁模型、误用行为、资源限制和可复现测试。每个已实现实验包含原理、代码入口、运行指令、结果解释、误区、安全边界、练习和一手来源。以解释深度和反例取代教程数量。

## 六大模块边界

| 模块 | 内容 | 交付标准与状态 |
| --- | --- | --- |
| 01 基础 | 对称/非对称、随机数/nonce/IV、AES、RSA、ECC、编码、哈希、签名、MAC | 本期概念入口；后续每节独立指南、例子、结果与误区 |
| 02 经典密码 | Caesar、Vigenère、单表替换、仿射、列置换、频率分析 | 本期 Caesar 与交互可视化；其余逐项增加测试 |
| 03 哈希与口令 | MD5、SHA-1/256/3、盐、PBKDF2/bcrypt/scrypt/Argon2id、历史彩虹表 | 本期三种 KDF；其他主题必须区分碰撞安全与口令猜测成本 |
| 04 安全实验室 | 合成口令、强度/熵局限、时间/内存、弱口令离线风险、管理器与 MFA | 本期有界基准；不接收外部凭据、不连接目标服务 |
| 05 CTF | 初/中/高级、自生成题、提示、数学推导、题解、答案、自动验证 | 未来每道题有独立数据和不泄露答案的题面，禁止伪称已实现 |
| 06 现代工程 | AES-GCM、RSA-OAEP/PSS、ECDH/HKDF、签名、随机性、密钥派生与管理 | 本期认证加密；后续使用成熟库与失败路径测试 |

## 架构与重要决策

1. 使用 `src/cryptosec_lab` 而非带连字符的源码目录，统一安装、导入、CLI 和 wheel 构建。文档使用主题目录；未实现的模块先在路线图明确标注，不创建虚假功能文件。
2. Python 3.11+；`cryptography` 提供 AESGCM，`argon2-cffi` 提供 Argon2id，标准库提供 scrypt/PBKDF2，`psutil` 测量进程 RSS。pytest、Ruff、build 作为开发依赖。
3. API 的类型、长度、记录版本和工作因子都有边界。AES 固定 256 位密钥、12 字节随机 nonce、最大 1 MiB 消息。大规模系统仍需 nonce 生命周期与密钥轮换策略。
4. KDF 固定教学参数：Argon2id 64 MiB/t=3/p=4（RFC 9106 低内存配置），scrypt N=16384/r=8/p=1，PBKDF2-HMAC-SHA256 100000 次。参数之间不等强度；后两者刻意保持教学资源可用，不能当作生产建议。
5. 基准仅动态生成一个合成口令用于每个进程的最多 5 轮测量。子进程串行、60 秒超时，报告实际样本和采样 RSS；不把 CPU 时间或 RSS 称为攻击成本。
6. 依赖由 pyproject 范围和精确 requirements-dev.lock 管理。更新要重跑测试、lint、打包、演示；Dependabot 提交更新 PR，由维护者审查，禁止自动发布。
7. MIT 许可；中英文入口；只放有效静态徽章。没有远程地址前不添加无法运行的仓库 CI/Stars 徽章。
8. 目标目录 `D:\GitHub\CryptoSec-Lab` 创建前不存在。此前工作目录的初稿保留；不删除原有文件。仅在目标目录初始化 Git，不设置远程、不创建公开仓库、不 push。
9. 首次提交署名采用用户提供的 Git 身份，仅配置于本仓库。提交元数据中的署名邮箱为用户授权使用，不写入教学文档。

## 目录

```text
CryptoSec-Lab/
  README.md / README_EN.md
  PROJECT_PLAN.md / TASKS.md / PROGRESS.md / CHANGELOG.md
  LICENSE / CONTRIBUTING.md / SECURITY.md
  pyproject.toml / requirements-dev.lock / .gitignore
  .github/workflows/ci.yml
  .github/ISSUE_TEMPLATE/ / PULL_REQUEST_TEMPLATE.md / dependabot.yml
  src/cryptosec_lab/       # 三个实验及 CLI、基准进程
  tests/                 # 已知向量、往返、认证失败、资源边界
  docs/                  # 模块指南、路线、社区、实际结果、发布说明
  docs/articles/         # 今天仅一篇可发布文章
  assets/caesar.html      # 本地离线交互演示
  scripts/check_repository.py
```

## 版本与验收

v0.1.0：三个 MVP 可安装、可运行，有真实验证记录和打包成果；v0.2.0：经典密码扩展；v0.3.0：合成口令与哈希教育；v0.4.0：CTF；v0.5.0：现代工程。遵循 SemVer，0.x API 可变更但必须记录。首次提交只提供本地发布候选，不创建远程 tag/Release。

每阶段汇报文件、命令、结果与下一步。失败须记录并修复，不以代码存在替代运行验证。GitHub 传播以每周一个经过验证的主题为单位，不承诺 Stars/Followers 数量。
