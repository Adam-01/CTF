import libnum
import sys

def lfsr(R, mask):
    output = (R << 1) & 0xffffff      #将R向左移动1位，bin(0xffffff) = '0b111111111111111111111111' = 0xffffff的二进制补码
    i = (R & mask) & 0xffffff         #按位与运算符&：参与运算的两个值,如果两个相应位都为1,则该位的结果为1,否则为0
    lastbit = 0
    while i != 0:
        lastbit ^= (i & 1)    #按位异或运算符：当两对应的二进位相异时，结果为1
        i = i >> 1
    output ^= lastbit
    return (output, lastbit)

mask = 0b1010011000100011100

f = open("key", "rb")   #以二进制追加模式打开
enc = libnum.s2n(f.read())
f.close()

for R in range(1000000, 16777216):
    s = ''

    if R % 10000 == 0:
        print(R)
    for i in range(12):
        tmp = 0
        for j in range(8):
            (R, out) = lfsr(R, mask)
            tmp = (tmp << 1) ^ out   #按位异或运算符：当两对应的二进位相异时，结果为1
        s += chr(tmp)
    if libnum.s2n(s) == enc:
        print(bin(R))
        sys.exit(0)
