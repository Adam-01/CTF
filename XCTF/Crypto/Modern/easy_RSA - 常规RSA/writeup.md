# easy_RSA

> 题目：在一次RSA密钥对生成中，假设p=473398607161，q=4511491，e=17，求解出d

EXP:
```python
import gmpy2

p = 473398607161
q = 4511491
e = 17

fn = (p - 1) * (q - 1)
d = gmpy2.invert(e, fn)
print(d)
```
