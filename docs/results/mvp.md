# MVP 实际运行记录

运行日期 2026-10-15，Windows 11，Python 3.12.14。仅验证了本机环境；GitHub 的 Linux/Windows 与 Python 3.11/3.12/3.13 矩阵尚未执行。

## 确定性演示

`cryptosec caesar`：`ciphertext_prefix="AOL XBPJR IYVDU MVE"`、`recovered_shift=7`、`roundtrip=true`、`frequency_recovery=true`。

`cryptosec aes`：`roundtrip=true`、`tamper_rejected=true`、`nonce_bytes=12`。运行中密钥随机生成且不记录。

## KDF 基准

命令 `cryptosec kdf --repeats 3`。全部原始样本、环境、参数在 [benchmark.json](benchmark.json)。以下均为实际测量，时间单位毫秒；内存为每 10 ms 采样的整个子进程树 RSS 总和峰值。

| 算法 | 哈希墙钟中位数 ms | CPU 中位数 ms | 采样峰值 MiB |
| --- | --- | --- | --- |
| Argon2id | 33.643 | 125.000 | 93.836 |
| scrypt | 140.738 | 140.625 | 45.410 |
| PBKDF2-HMAC-SHA256 | 20.511 | 15.625 | 30.180 |

Argon2id 并行度为 4，CPU 时间高于墙钟时间是可能的。此表不是同等安全强度的速度排名；参数固定且不同，RSS 含解释器、库、启动器和验证，也可能重复计算共享页。首次测量只跟踪 Windows 启动器，发现约 4 MiB 的异常低值后已修正为整个进程树并重跑；上表采用修正后的结果。

最终自动化测试、代码检查及打包记录见 [PROGRESS.md](../../PROGRESS.md)。
