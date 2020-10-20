# 最优非加密对称填充（OAEP）

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

with open('pubkey.pem', 'r') as f:
    key = RSA.importKey(f.read())
    n = key.n
    e = key.e

print("n =", n)
print("e =", e)

with open('private.pem', 'r') as f:
    private = RSA.importKey(f.read())
    oaep = PKCS1_OAEP.new(private)

with open('flag.enc', 'rb') as f:
    print(oaep.decrypt(f.read()).decode())