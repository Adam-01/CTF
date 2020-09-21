# base64stego

> 把base64字符串最后一个字节（符）的可利用bit连接起来，以每8bits一个字节


POC:  

```python
base64chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
flag = ''

with open('stego.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        line.strip()
        num = line.count('=')   # 判断有多少个等号
        if num == 0:
            continue
        lastchar = line[line.index('=') - 1]    # 取得等号前的最后一个字符

        myindex = base64chars.index(lastchar)
        bin_str = bin(myindex).replace('0b', '').zfill(6)
        flag += bin_str[6 - 2 * num:]       # 取得可用的bits（4个或2个）
    print(flag)

# 每8bits凑成一个字节
i = 0
for j in range(len(flag)):
    print(chr(int(flag[i:i+8], 2)), end='')
    i += 8
