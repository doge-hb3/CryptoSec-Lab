# 口令哈希：盐、成本与可复现测量

## 为什么不直接 SHA-256

哈希不提供用密钥恢复明文的解密接口，但攻击者仍可猜测输入并比对。MD5/SHA-1 的碰撞安全已失效；即使换成抗碰撞更好的 SHA-256，普通快速哈希仍不能显著增加口令猜测成本。碰撞攻击和猜测某个用户口令是不同问题。

独立随机盐让相同口令产生不同记录，阻止跨用户复用预计算结果。盐无需保密，不能阻止针对单条记录继续猜测；彩虹表是以时间/存储折中预计算映射的历史方案，随机盐使通用表复用变得不现实。口令 KDF 进一步增加每次猜测的时间或内存需求。

## 当前固定参数

| 算法 | 参数 | 说明 |
| --- | --- | --- |
| Argon2id | 65536 KiB, t=3, p=4 | RFC 9106 低内存配置，编码串带盐和参数 |
| scrypt | N=16384, r=8, p=1, 32 字节输出 | 主内存项约 128Nr=16 MiB，OpenSSL maxmem=32 MiB |
| PBKDF2 | HMAC-SHA256, 100000 次, 32 字节输出 | CPU 成本教学基线，不是生产推荐 |

后两者选用较低成本方便本地教学。配置不是等安全性的比较，也不是当前部署标准。生产环境需参考最新规范、硬件、并发容量和延迟预算重新选择并制定升级策略。

```python
from cryptosec_lab.passwords import hash_password, synthetic_password, verify_password

password = synthetic_password()
record = hash_password(password, "argon2id")
print(verify_password(password, record))
print(verify_password(password + "!", record))
```

输出 `True`、`False`。每次创建记录使用新盐；不打印口令或把运行记录当测试凭据。源码在 [passwords.py](../../src/cryptosec_lab/passwords.py)。记录版本固定参数；Argon2 验证前检查编码参数，防止恶意记录要求巨大内存。scrypt/PBKDF2 使用独立 16 字节盐及常量时间摘要比较。

## 性能实验

运行 `cryptosec kdf --repeats 3`，三个子进程串行执行，每个生成一个合成口令，重复哈希并验证。最多 5 次，进程超时 60 秒；正常参数下工作集最高的一项为 Argon2id 的 64 MiB，解释器等另占内存。无外部目标与外部凭据参数。

`hash_ms` 是全部实际哈希样本，`median_hash_ms` 为中位数，`median_cpu_ms` 为进程 CPU 时间中位数。计时不包含验证；第一轮包含冷启动内部开销，无预热。父进程每 10 ms 采样整个子进程树的 RSS 总和（包括 Windows 虚拟环境启动器及实际解释器），字段为 `sampled_peak_process_tree_rss_mib`；峰值包括解释器、导入、哈希及验证，可能漏掉短峰值或重复计算共享页，不是算法独占内存或整个机器的峰值。CPU 并行时 CPU 时间可以高于墙钟时间。不同硬件结果不可直接推广。[本次实测](../results/mvp.md)仅供复现。

## 熵与防护

`L log2(N)` 只适用于从 N 个字符独立均匀抽样的生成模型，不能从人写的密码长度推断真实熵。长而随机的密码或由密码学安全方式抽样的口令短语更可预测地提高搜索成本。使用密码管理器生成独立口令，配合 MFA 降低单一口令泄漏的影响；MFA 并不自动解决钓鱼和会话盗用。

练习：比较 1 次和 5 次测量，解释波动及为什么最快的算法不等于最佳存储策略。bcrypt、摘要族和小规模离线弱口令演示列入后续路线，当前未实现。

来源：[RFC 9106](https://www.rfc-editor.org/rfc/rfc9106.html)、[argon2-cffi API](https://argon2-cffi.readthedocs.io/en/stable/api.html)、[Python hashlib](https://docs.python.org/3/library/hashlib.html)。
