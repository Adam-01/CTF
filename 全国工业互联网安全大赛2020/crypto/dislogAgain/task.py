from gmpy2 import *
from Crypto.Util.number import bytes_to_long
import random
from secret import flag

def keygen():
    p = next_prime(random.getrandbits(1024))
    q = next_prime(p**3)
    n = p*p*q
    tmp = p*p
    while True:
        g = random.randint(2,n-1)
        if pow(g,p-1,tmp) != 1:
            break
    return g,n,p,q


def encrypt(g,n,msg,p):
    msg = bytes_to_long(msg)
    assert(msg<p)
    r = random.randint(1,n-1) 
    h = pow(g,n,n)

    return (pow(g,msg,n)*pow(h,r,n))%n

g,n,p,q = keygen()

print g
print n
print encrypt(g,n,flag,p)

