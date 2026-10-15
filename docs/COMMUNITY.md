# GitHub 展示与社区

## 首页设置建议

Description：`Hands-on cryptography and password security labs in Python: Caesar analysis, AES-GCM, and bounded KDF benchmarks. 中文 / English.`

Topics（选择实际相关项，控制在 12 个左右）：`cryptography`, `python`, `cybersecurity`, `education`, `aes-gcm`, `argon2`, `scrypt`, `pbkdf2`, `password-security`, `classical-cipher`, `frequency-analysis`, `chinese`。CTF 尚未交付，不优先用它吸引搜索。

英文搜索词自然用于专题标题：authenticated encryption、password hashing、Caesar cipher frequency analysis、Python KDF benchmark。中文词：密码学教学、认证加密、凯撒密码、口令哈希、加盐、密钥派生、密码安全实验。用教程真实回答问题，不重复堆词。

入口顺序：定位 → 已实现模块 → 快速运行 → 示例与可视化 → 路线/进度 → 贡献 → 安全和许可。远程上线并通过 CI 后，再添加指向真实工作流的 CI 徽章；不伪造 Stars、下载量或贡献者。

## Discussions 与首批任务

仓库上线后由维护者启用 Discussions。建议分类：Announcements（维护者发布）、Q&A（允许标记答案）、Ideas（实验提案）、Show and tell（合成实验结果）。当前未在远程创建任何分类或 Issue。

| 建议任务 | 标签 | 明确验收 |
| --- | --- | --- |
| 为 Caesar 增加短文本排名失败的固定样例 | good first issue, tests | 不声称每条英文都可正确恢复，测试覆盖全部候选 |
| 改善离线演示的键盘操作提示 | good first issue, accessibility | 不用鼠标也能完成移位，保留零网络请求 |
| 英译 AES-GCM 专题 | documentation | 命令、异常与参数同源码一致 |
| 添加 scrypt 参数解释图 | documentation | 标清理论主内存与进程 RSS 不同 |
| 新增仿射密码实验 | enhancement | 模逆条件、已知向量、非互质拒绝测试 |

## 可持续传播

每周围绕一个已验证主题写一篇说明或更新；本次只准备一篇文章。先在仓库 `docs/articles` 保存可追踪版本，再由维护者决定发布为 Discussion 或技术博客。技术问答仅在问题相关时给出解释和链接；不批量私信、刷星、购买关注或重复发广告。

收集有价值的使用反馈：复现成功率、文档命令错误、外部贡献被合并的原因、问题解决时间；Stars/Forks/Followers 作为被动观察，不设置增长承诺。每次 Release 附真实改变、验证环境、升级提示和下一步反馈入口。
