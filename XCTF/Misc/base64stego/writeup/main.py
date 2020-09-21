import base64

base64chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
flag = ''

with open('../stego.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        line.strip()
        num = line.count('=')
        if num == 0:
            continue
        lastchar = line[line.index('=') - 1]

        myindex = base64chars.index(lastchar)
        bin_str = bin(myindex).replace('0b', '').zfill(6)
        flag += bin_str[6 - 2 * num:]
    print(flag)

i = 0
for j in range(len(flag)):
    print(chr(int(flag[i:i+8], 2)), end='')
    i += 8