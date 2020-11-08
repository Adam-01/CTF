base64chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

flag = ''

with open('stego.txt', 'r') as f:
    lines = f.readlines()
    
for line in lines:
    num = line.count('=')   # 判断有多少个等号
    if num == 0:
        continue
    lastchar = line[line.index('=') - 1]    # 取得等号前的最后一个字符

    index = base64chars.index(lastchar)
    bin_str = bin(index).replace('0b', '').zfill(6)   # 保证二进制串刚好6位
    flag += bin_str[-2 * num:]     # 取得可用的bits（4个或2个），两个等号可藏4个bit，一个等号可藏2个bit

# 每8bits凑成一个字节
i = 0
for j in range(len(flag) // 8):
    print(chr(int(flag[i:i+8], 2)), end='')
    i += 8