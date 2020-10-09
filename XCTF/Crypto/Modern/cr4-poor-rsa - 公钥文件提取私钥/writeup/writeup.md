# cr4-poor-rsa

> 题目有两个文件flag.b64和key.pub

1. 先把flag.b64转换成字节类型的文件
```python
import base64

with open('flag.b64', 'r') as f:
    with open('flag.enc', 'wb') as fw:
        text = base64.b64decode(f.readline().encode())
        fw.write(text)
```

2. 使用openssl读取公钥
```bash
openssl -pubin -text -modulus -in key.pub
```
模数：n = 833810193564967701912362955539789451139872863794534923259743419423089229206473091408403560311191545764221310666338878019  
指数：e = 65537  

3. 分解模数modulus(n)
p = 863653476616376575308866344984576466644942572246900013156919  
q = 965445304326998194798282228842484732438457170595999523426901  

4. 使用rsatool.py生成私钥
```bash
rsatool.py -o private.pem -p 863653476616376575308866344984576466644942572246900013156919 -q 965445304326998194798282228842484732438457170595999523426901 -e 65537
```

5. 使用openssl解密密文
```bash
openssl rsautl -decrypt -inkey private.pem -in flag.enc 
```