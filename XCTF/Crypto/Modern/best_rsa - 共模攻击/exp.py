import Crypto
from Crypto.PublicKey import RSA
import gmpy2
import libnum

with open('publickey1.pem', 'r') as f:
    pubkey1 = Crypto.PublicKey.RSA.importKey(f.read())
with open('publickey2.pem', 'r') as f:
    pubkey2 = Crypto.PublicKey.RSA.importKey(f.read())
with open('cipher1.txt', 'rb') as f:
    c1 = libnum.s2n(f.read())
with open('cipher2.txt', 'rb') as f:
    c2 = libnum.s2n(f.read())

assert pubkey1.n == pubkey2.n

n = pubkey1.n
e1 = pubkey1.e
e2 = pubkey2.e

# 扩展欧几里得算法
gcd, s1, s2 = gmpy2.gcdext(e1, e2)

if s1 < 0:
    s1 = -s1
    c1 = gmpy2.invert(c1, n)
if s2 < 0:
    s2 = -s2
    c2 = gmpy2.invert(c2, n)

# 求得c1，s1，c2，s2，代入
m = pow(c1, s1, n) * pow(c2, s2, n) % n

print(libnum.n2s(int(m)).decode())
