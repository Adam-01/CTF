# 2EM

> 题目描述：One round EM is unsafe, so two round EM is safe?

题目给出了task.py和data两个文件，data文件前11行每行打印出一个数字，后面打印出两个数字。  

根据题目代码：
```python
flag = flag.ljust(44, b'\x00')

for i in range(len(flag) / 4):
    pass
```
可推测，前11行打印的是第一个for循环
```python
print(encrypt(key,pt))
```
后面行打印的是第二个for循环
```python
print(pt, ct)
```

我们使用data文件中的第12行，pt = 3972024911，ct = 3661089527，由于key是由random.getrandbits(32)生成的，即key的密钥空间是2^32（4294967296），42亿多。  

我们用正面爆破的方式解出key，爆破脚本如下：
```python
import random

pt = 3972024911
ct = 3661089527

def encrypt(key, msg):
    tmp1 = p(msg ^ key, pbox1)
    tmp2 = p(tmp1 ^ key, pbox2)
    return (tmp2 ^ key)

for key in range(4294967296):
    if key % 100000 == 0:
        print(key)
    result = encrypt(key, pt)
    if result == ct:    # 如果结果相等
        print('key:', key)
        break
```
大概跑了三个多小时，解出key=2091272121  

然后，根据encrypt()函数，return (tmp2 ^ key)，已知key和前11行数据，可以用key和前11行数据进行异或，得出encrypt()函数中的每个tmp2  

根据p(data, pbox)函数，它的意思是用pbox中的位置，来打乱data用二进制来表示的顺序，比如，pbox2 = [17, 6, 7, 27, 4, 20, ...]，就是取data的第17位作为out的第1位，第6位作为out的第2位，第7位作为out的第3位，等等，那么可以据此得到复原的顺序。脚本如下：
```python
pbox1 = [22, 28, 2, 21, 3, 26, 6, 14, 7, 16, 15, 9, 17, 19, 8, 11, 10, 1, 13, 31, 23, 12, 0, 27, 4, 18, 30, 29, 24, 20, 5, 25]
pbox2 = [17, 6, 7, 27, 4, 20, 11, 22, 2, 19, 9, 24, 23, 31, 15, 10, 18, 28, 5, 0, 16, 29, 25, 8, 3, 21, 30, 12, 14, 13, 1, 26]

for i in range(len(pbox1)):
    print(pbox1.index(i), end=', ')

for i in range(len(pbox2)):
    print(pbox1.index(i), end=', ')
```
上面脚本的意思是，按0-31的顺序找到各自出现的位置，把这些位置作为pbox加密函数的逆函数。比如pbox1中，0出现在第22位，1出现在第17位等等。  

据此得到
```python
pbox1_reverse = [22, 17, 2, 4, 24, 30, 6, 8, 14, 11, 16, 15, 21, 18, 7, 10, 9, 12, 25, 13, 29, 3, 0, 20, 28, 31, 5, 23, 1, 27, 26, 19]
pbox2_reverse = [19, 30, 8, 24, 4, 18, 1, 2, 23, 10, 15, 6, 27, 29, 28, 14, 20, 0, 16, 9, 5, 25, 7, 12, 11, 22, 31, 3, 17, 21, 26, 13]
```

然后，根据encrypt()函数，和上面得出的每个msg的tmp2，可以写出整个encrypt()函数的逆函数，即解密函数：
```python
import libnum

# 用前11行的数据与key异或，得到flag0-10
flag0 = 3816895236
flag1 = 4255101616
flag2 = 3787662148
flag3 = 763377169
flag4 = 2211231701
flag5 = 731128563
flag6 = 534590180
flag7 = 298984004
flag8 = 1842263665
flag9 = 466400113
flag10 = 4156952853

key = 2091272121

pbox1 = [22, 28, 2, 21, 3, 26, 6, 14, 7, 16, 15, 9, 17, 19, 8, 11, 10, 1, 13, 31, 23, 12, 0, 27, 4, 18, 30, 29, 24, 20, 5, 25]
pbox2 = [17, 6, 7, 27, 4, 20, 11, 22, 2, 19, 9, 24, 23, 31, 15, 10, 18, 28, 5, 0, 16, 29, 25, 8, 3, 21, 30, 12, 14, 13, 1, 26]
#print(bin(3816895236)[2:])

pbox1_reverse = [22, 17, 2, 4, 24, 30, 6, 8, 14, 11, 16, 15, 21, 18, 7, 10, 9, 12, 25, 13, 29, 3, 0, 20, 28, 31, 5, 23, 1, 27, 26, 19]
pbox2_reverse = [19, 30, 8, 24, 4, 18, 1, 2, 23, 10, 15, 6, 27, 29, 28, 14, 20, 0, 16, 9, 5, 25, 7, 12, 11, 22, 31, 3, 17, 21, 26, 13]

flag_all = [flag0, flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8, flag9, flag10]
# print(len(bin(763377169)))

# 分组解密
for flag_i in flag_all:
    tmp = ''
    for i in pbox2_reverse:
        tmp += bin(flag_i)[2:].rjust(32, '0')[i]
        #print(tmp)
    #print(tmp, end='')
    tmp1 = int(tmp, 2) ^ key
    #print(bin(tmp1)[2:])

    tmp3 = bin(tmp1)[2:].rjust(32, '0')
    #print(tmp3)

    tmp = ''
    for j in pbox1_reverse:
        tmp += tmp3[j]
    flag = int(tmp, 2) ^ key
    print(libnum.n2s(flag).decode(), end='')

# flag{843f4cf5-8edc-49e7-9fd2-7cb31840c10f}
```

完  