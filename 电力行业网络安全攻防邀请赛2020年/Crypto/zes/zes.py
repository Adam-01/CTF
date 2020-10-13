import os
import operator
from Crypto.Util.number import long_to_bytes,bytes_to_long,getPrime
from Crypto.Cipher import AES
flag=open("flag","rb").read()

def f(m,k):
    h=AES.new(k,AES.MODE_ECB)
    return h.encrypt(m)

def fso(b):
    l=b[0:16]
    r=b[16:32]
    nl=r
    nr=f(bytes(map(operator.xor, l, r)),r)
    return nl+nr

def fs(b):
    r=b
    for _ in range(16):
        r=fso(r)
    return r

iv=os.urandom(16)
key=os.urandom(16)
h=AES.new(key,AES.MODE_CBC,iv)
print(h.encrypt(flag).hex())
c=fs(iv+key)

ag=[]
ag.append(getPrime(128))
for _ in range(3):
    ag.append(bytes_to_long(os.urandom(16)))
print(ag[0:3])
seed=ag[3]


for i in range(20):
    ag[3]=(ag[1]*ag[3]+ag[2]) % ag[0] #st=(at*st+bt)%mt
    print(ag[3]>>64,end=',')
print("")

print(bytes(map(operator.xor, c, long_to_bytes(seed)+long_to_bytes(seed))).hex())