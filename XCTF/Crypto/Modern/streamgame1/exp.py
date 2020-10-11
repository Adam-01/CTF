import libnum

mask = 0b1010011000100011100

def lfsr_reverse(output, lastbit):
    output ^= lastbit

    while lastbit != 0:
        i = i << 1
        lastbit ^= (i & 1)

    R = (output & 0xffffff) >> 1
    mask = (i & 0xffffff) & R

    return (R, mask)

with open('key', 'rb') as f:
    s = f.read()
print(s)

lastbit = 0
for i in range(len(s)):
    tmp = int(hex(s[i]), 16)
    for i in range(12):
        for j in range(8):
            out = tmp ^ (tmp >> 1)
            (R, mask) = lfsr_reverse(R, output)
    print(R)