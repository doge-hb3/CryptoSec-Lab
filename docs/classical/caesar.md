# Caesar：从可逆移位到统计泄漏

## 原理

把 ASCII 字母映射到 0–25：加密 `c=(p+k) mod 26`，解密 `p=(c-k) mod 26`。大小写分别保留，中文、数字、空格、标点原样保留。本实现[源码](../../src/cryptosec_lab/classical.py)限制 100000 字符，移位必须为整数，拒绝布尔值。

```python
from cryptosec_lab.classical import analyze, decrypt, encrypt

print(encrypt("Attack at dawn!", 3))
print(decrypt("Dwwdfn dw gdzq!", 3))
text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG. " * 8
best = analyze(encrypt(text, 7))[0]
print(best.shift, best.plaintext == text)
```

输出为 `Dwwdfn dw gdzq!`、`Attack at dawn!`、`7 True`。直接执行 `cryptosec caesar` 可复现对应样例。

## 分析与可视化

只存在 26 个不同移位（包含恒等移位），可全部检查。频率法对每个候选明文计算 `Σ(观察次数−期望次数)²/期望次数`，以常见英语字母频率为期望分布，值较小者先检查。实现复用密文字母计数，返回全部候选及分数。没有 ASCII 字母时拒绝分析。

浏览器打开 [assets/caesar.html](../../assets/caesar.html)，输入自定义教学文本，拖动滑块，观察原/密文字母对应和柱状频数平移。页面离线运行且限制 2000 字符。

## 误区与练习

频率排名不是密码学证明；短文本、专业缩写、非英语文本和人为构造的字母分布会误导排序。本例 pangram 重复只是固定演示，不代表自然语言的完整分布。把 8 次重复改为一个单词，手工比较 26 个候选；记录最优分数是否仍对应真实密钥。

Caesar 不适合保护真实信息，增加移位数值不能增加模 26 后的密钥空间。现代保密请使用[认证加密](../modern/aes-gcm.md)。英语频率启发式仅用于自己生成的数据。
