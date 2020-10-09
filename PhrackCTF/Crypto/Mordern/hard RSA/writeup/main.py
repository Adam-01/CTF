import gmpy2
import rsa

n = 0xC2636AE5C3D8E43FFB97AB09028F1AAC6C0BF6CD3D70EBCA281BFFE97FBE30DD

# yafu.exe factor(87924348264132406875276140514499937145050893665602592992418171647042491658461)
p = 319576316814478949870590164193048041239
q = 275127860351348928173285174381581152299
fn = (p - 1) * (q - 1)

e = 2
'''
d = int(gmpy2.invert(e, fn))

prikey = rsa.PrivateKey(n, e, d, p, q)

with open('flag.enc', 'rb') as f:
    c = f.read()
m = rsa.decrypt(c, prikey).decode()
'''

k = 0
with open('flag.enc', 'rb') as f:
    c = int(bytes.hex(f.read()), 16)

import math
print(hex(int(math.sqrt(c))))



'''
while True:
    print(k)
    if(gmpy2.iroot(c + n * k, 2)[1] == True):
        print(gmpy2.iroot(c + n * k, 2))
        break
    k += 1
'''