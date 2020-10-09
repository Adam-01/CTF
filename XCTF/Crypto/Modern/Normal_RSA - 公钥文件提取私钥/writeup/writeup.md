# Normal_RSA

> 题目：公钥文件pubkey.pem，密文文件flag.enc

1. 获得公钥的模数n
```bash
openssl rsa -pubin -text -modulus -in pubkey.pem 
```

分解n，得到p、q  
```python
import gmpy2

n = 87924348264132406875276140514499937145050893665602592992418171647042491658461

# 分解n得到p、q
p = 275127860351348928173285174381581152299
q = 319576316814478949870590164193048041239
fn = (p - 1) * (q - 1)
e = 65537

d = gmpy2.invert(e, fn)
```

2. 生成私钥
```bash
rsatool.py -o private.pem -p 275127860351348928173285174381581152299 -q 319576316814478949870590164193048041239 -e 65537
```

3. 解密文件
```bash
openssl rsautl -decrypt -inkey private.pem -in flag.enc
```