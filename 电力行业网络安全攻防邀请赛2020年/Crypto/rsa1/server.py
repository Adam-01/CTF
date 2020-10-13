#!/usr/bin/python
# encoding: utf-8
import random
import sys
import os
from hashlib import sha256,sha512
from Crypto.Util.number import *
from Crypto.PublicKey import RSA
from binascii import b2a_hex, a2b_hex
import random
import binascii
from pyDes import des, PAD_PKCS5, ECB
#from secret import flag
#flag=b'flag{4ce36138-fd4c-11ea-9083-dca90498a2db}'
with open('/flag','rb') as f:
    flag = f.read()


def des_en(msg,secret_key):
    iv =secret_key
    key = des(secret_key, ECB, iv, pad=None, padmode=PAD_PKCS5)
    entrymsg = key.encrypt(msg, padmode=PAD_PKCS5)
    return binascii.b2a_hex(entrymsg)


def my_print(message):
    sys.stdout.write('{0}\n'.format(message))
    sys.stdout.flush()
    sys.stderr.flush()

def read_str():
    return sys.stdin.readline().strip()

def read_int():
    return int(sys.stdin.readline().strip())

def proof_of_work():
    s = os.urandom(3)
    hx1 = os.urandom(20)
    digest = sha256(s+hx1).hexdigest()
    print("sha256(XXX + {0}) == {1}".format(hx1.hex(),digest))
    my_print("Give me XXX in hex: ")
    x = read_str()
    if len(x) != 6 or x != s.hex():
        print("Wrong!")
        return False
    return True

def PoW():
    if not proof_of_work():
        exit(-1)
def challenge1():
    key  = bytes(os.urandom(10).hex(),'utf8')
    m = bytes_to_long(b'key:'+ key)
    p = getPrime(1024)
    q =  getPrime(1024)
    n = p * q
    for i in range(2):
        e = getPrime(150)
        my_print('e='+str(e))
        my_print('n='+str(n))
        my_print('c='+str(pow(m,e,n)))
        
    my_print("Give me the key: ")
    x = read_str()
    if x != str(key)[2:-1]:
        my_print('Wrong!')
        exit(-1)
    
        
def challenge2():
    key  = bytes(os.urandom(10).hex(),'utf8')
    m = bytes_to_long(b'key:'+ key)
    p = getPrime(1024)
    q =  getPrime(1024)
    n = p * q
    e = 5
    c = pow(m,e,n)
    my_print('e='+str(e))
    my_print('n='+str(n))
    my_print('c='+str(pow(m,e,n)))    
    
    my_print("Give me the key: ")
    x = read_str()
    if x != str(key)[2:-1]:
        my_print('Wrong!')
        exit(-1)
        



def print_flag():
    key = random.randint(10000000,10999999)
    c = des_en(flag,str(key))

    my_print('key:10000000-10999999')
    my_print('c:'+ str(c)[2:-1])


if __name__ == '__main__':
    PoW()
    challenge1()
    challenge2()
    print_flag()
    
        
    
