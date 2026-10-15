# AES-GCM：密文能解开，还必须确认未被篡改

## 原理与接口

GCM 把 AES 的计数器加密与认证结合。`cryptography.AESGCM` 返回密文及 16 字节标签；同一密钥下 nonce 必须唯一。AAD 是参与认证但不加密的上下文，如消息类型和版本。[源码](../../src/cryptosec_lab/modern.py)固定 AES-256、12 字节随机 nonce，数据上限 1 MiB；`Envelope` 保存 nonce 与带标签的密文，密钥由调用者单独保管。

```python
from cryptosec_lab.modern import decrypt, encrypt, new_key

key = new_key()
message = encrypt(key, b"CryptoSec-Lab", b"lesson:01")
print(decrypt(key, message, b"lesson:01"))
```

输出 `b'CryptoSec-Lab'`。执行 `cryptosec aes`，观察 `roundtrip=true`、`tamper_rejected=true`、`nonce_bytes=12`；密钥和密文每次变化，不把随机输出当作固定向量。

## 实验与失败路径

将密文任一字节异或 1，解密应抛出 `InvalidTag`。错误密钥、变更 nonce、截断密文、错误 AAD 均有测试，另以库直接调用验证互操作。认证异常不得忽略，不得返回部分明文。

## 误区与安全实践

nonce 不是秘密，也不是密钥。随机 96 位 nonce 仍有生日碰撞风险，不能无限复用同一密钥；生产系统应规定每钥消息量、轮换、并发 nonce 分配与持久化策略。本实验不提供完整密钥管理。AAD 可以阻止跨上下文替换，但本身不实现防重放；协议还需序列号及接收端状态。真实密码不能直接编码后作为 AES 密钥。

练习：把解密 AAD 改成 `b"lesson:02"`，确认抛出认证异常，再解释它为何不是普通解码错误。

来源：[cryptography AESGCM API](https://cryptography.io/en/stable/hazmat/primitives/aead/)。
