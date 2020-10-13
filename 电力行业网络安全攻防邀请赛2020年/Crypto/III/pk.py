import binascii
from math import gcd
import gmpy
from flag import flag
from random import randint


class pks:
    def __init__(self):
        self.mxl = 28
        
    def gen_key(self):
        self.pkt = [randint(1,10)]

        for i in range(8 * self.mxl - 1):
            s = sum(self.pkt)
            self.pkt.append(s + randint(s, s*3))

        s = sum(self.pkt)
        self.m1 = randint(s, s*3)

        self.m2 = randint(1,self.m1)
        while gcd(self.m2,self.m1) != 1:
            self.m2 = randint(1,self.m1)

        self.pubkey = list(map(lambda x : self.m2 * x % self.m1, self.pkt))

    def encrypt(self,msg):
        if len(msg)  > 30:
            return ''
        binary = bin(int(binascii.hexlify(msg),16))[2:]
        l = len(binary)
        if l % 8 != 0:
            binary = binary.rjust(l + (8-(l%8)),'0')
        c = 0
        for i in range(len(binary)):
            if binary[i] == '1':
                c += self.pubkey[i]
        return hex(c)[2:]

    def decrypt(self,enc):
        enc = int(enc,16)
        inv = int(gmpy.invert(self.m2, self.m1))
        m = inv * enc % self.m1
        s = ''
        for i in reversed(self.pkt):
            if m >= i:
                m -= i
                s += '1'
            else:
                s += '0'
        s = binascii.unhexlify(hex(int(s[::-1],2))[2:])
        return s

p = pks()
p.gen_key()
print('p : ' + str(p.pubkey))
print('e: ' + p.encrypt(flag))
