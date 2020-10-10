import gmpy2
import libnum

n = 0xC2636AE5C3D8E43FFB97AB09028F1AAC6C0BF6CD3D70EBCA281BFFE97FBE30DD

# yafu.exe factor(87924348264132406875276140514499937145050893665602592992418171647042491658461)
p = 319576316814478949870590164193048041239
q = 275127860351348928173285174381581152299
fn = (p - 1) * (q - 1)

e = 2

with open('flag.enc', 'rb') as f:
    c = libnum.s2n(f.read())

c1 = pow(c, (p + 1) // 4, p)
c2 = pow(c, (q + 1) // 4, q)
cp1 = p - c1
cp2 = q - c2
t1 = gmpy2.invert(p, q) # p的模q逆元
t2 = gmpy2.invert(q, p) # q的模p逆元

m1 = (q * c1 * t2 + p * c2 * t1) % n
m2 = (q * c1 * t2 + p * cp2 * t1) % n
m3 = (q * cp1 * t2 + p * c2 * t1) % n
m4 = (q * cp1 * t2 + p * cp2 * t1) % n

for i in (m1, m2, m3, m4):
    m = '%x' % i
    if len(m) % 2 == 1:
        m = '0' + m     # padding
    print(libnum.n2s(int(m, 16)))