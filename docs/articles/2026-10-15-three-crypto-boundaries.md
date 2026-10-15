# 从凯撒密码到 AES-GCM：用三个 Python 实验理解密码学边界

2026-10-15 · CryptoSec-Lab 首篇学习记录 · 待维护者发布

今天的学习从一个简单问题开始：程序能把字符串变回原文，就说明它安全吗？三个本地实验给出了不同层次的答案。所有代码都在项目中，可以通过 `cryptosec caesar`、`cryptosec aes` 和 `cryptosec kdf --repeats 3` 重现；使用的口令由程序生成。

## 可逆并不意味着难以破解

凯撒密码把英文字母移位。`Attack at dawn!` 移位 3 后得到 `Dwwdfn dw gdzq!`，反向移动即可恢复。整数移位最终对 26 取模，因此只有 26 个候选。实现并不复杂，问题在于密钥空间太小，同时字母频率只是整体移动，原文的统计结构仍在。

实验枚举所有候选，并比较它们与常见英语频率的卡方距离。固定长样例的正确移位被排在第一位，但这不能推广到任意文本。一个名字、缩写或中文片段没有足够的英语统计信息。展示完整候选和失败条件，比写“自动破解所有凯撒密码”更能解释算法的能力。

## 保密性之外还需要认证

第二个实验使用成熟密码学库的 AES-GCM。密钥在内存中随机生成，每次加密生成 12 字节 nonce，认证标签与密文一起返回。额外的 `lesson:01` 作为 AAD 参与认证，不加密。把密文改动一个比特，再尝试解密，库会抛出 `InvalidTag`。

```python
from cryptosec_lab.modern import decrypt, encrypt, new_key

key = new_key()
message = encrypt(key, b"CryptoSec-Lab", b"lesson:01")
assert decrypt(key, message, b"lesson:01") == b"CryptoSec-Lab"
```

这揭示了一个工程细节：错误密钥、消息篡改和上下文不一致都必须使接收端拒绝消息。不能忽略认证异常后继续使用数据。nonce 不需要保密，但同一密钥下不能重复；随机生成也有碰撞概率，生产系统仍要管理消息量和轮换。AAD 绑定上下文，本身并不提供防重放。

## 口令存储不能只看算法名字

第三个实验比较 Argon2id、scrypt 和 PBKDF2。口令哈希没有解密接口，但攻击者可以猜输入、运行同一函数、比较输出。普通 SHA-256 运行很快，加盐可以破坏通用预计算复用，却不能阻止逐条猜测。因此还需要增加单次尝试的成本。

基准逐个启动独立进程，每种算法只处理程序生成的合成口令，最多测量五轮。记录哈希墙钟时间、CPU 时间和进程 RSS。Argon2id 使用 RFC 9106 的低内存配置；scrypt 和 PBKDF2 使用方便教学的固定成本，不能把三者的速度排名当成相同安全强度下的比较。

RSS 包含解释器、库和验证过程，10 毫秒采样也可能漏掉峰值。这些测量帮助理解资源代价，而不是精确预测攻击者每秒能猜多少次。真正部署时还要考虑并发负载、延迟预算、参数升级、密码管理器与 MFA。

## 今天可以复用的成果

项目提供三个真实可运行的 CLI、自动化测试、离线 Caesar 可视化和中英文入口。后续计划逐步加入 Vigenère、仿射密码、自生成 CTF、RSA-OAEP/PSS 及 ECDH/HKDF。本次只发布这一篇文章，不把计划中的功能写成已经交付。

建议读者先运行实验，再修改一个参数或输入，预测失败条件。能够解释为什么某个样例失败，是从“会调用函数”走向理解密码工程的一步。

资料：[cryptography AESGCM](https://cryptography.io/en/stable/hazmat/primitives/aead/)、[RFC 9106](https://www.rfc-editor.org/rfc/rfc9106.html)、[Python hashlib](https://docs.python.org/3/library/hashlib.html)。项目入口见仓库根目录 README；首次发布时由维护者添加真实仓库链接。
