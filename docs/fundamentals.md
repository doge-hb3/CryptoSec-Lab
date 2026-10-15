# 先区分四类工具

对称加密用同一秘密密钥加解密；非对称密码使用公钥/私钥，但加密、签名和密钥交换是不同机制。AES 是 128 位分组的对称密码，AES-GCM 是带认证的使用方式；RSA 需要 OAEP/PSS 等编码方案；ECC 基于椭圆曲线群上的数学问题，通常以 ECDH 交换密钥或 ECDSA/EdDSA 签名。MVP 未实现后三者，专题在路线中。

编码改变表示，没有密钥门槛。哈希把任意长度输入映射为定长摘要，没有“解密”操作；猜测输入并比较摘要属于搜索。MAC 用共享密钥认证消息；数字签名用私钥签名、公钥验证，不能单凭签名隐藏内容。加密的可逆性、哈希的抗原像性和签名的不可伪造性是不同目标。

运行（已安装环境）：

```python
import base64
import hashlib

print(base64.b64encode(b"hello").decode())
print(hashlib.sha256(b"hello").hexdigest())
```

输出分别为 `aGVsbG8=` 与 `2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824`。Base64 可直接解码；摘要不是压缩后的可恢复密文。

随机数应使用 `secrets` 等密码学安全源。Nonce 关注在协议要求下不重复；IV 的要求因模式而异，不能一概而论；盐是公开的每条记录随机值，改变口令派生结果。不要用盐当 AES 密钥，也不要把 nonce、IV、盐统称为秘密。

误区：RSA 公钥加密并不证明发送者身份；哈希不能代替带密钥的认证；随机 nonce 的碰撞概率不是零；口令长度只在生成模型明确时才能转换为熵。下一步阅读各实验具体边界。

来源：[Python hashlib](https://docs.python.org/3/library/hashlib.html)、[cryptography AEAD](https://cryptography.io/en/stable/hazmat/primitives/aead/)。
