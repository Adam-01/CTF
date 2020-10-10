import gmpy2
import libnum

# openssl rsa -pubin -text -modulus -in pubkey.pem
n = 0xC2636AE5C3D8E43FFB97AB09028F1AAC6C0BF6CD3D70EBCA281BFFE97FBE30DD
e = 65537

# yafu.exe factor(87924348264132406875276140514499937145050893665602592992418171647042491658461)
p = 319576316814478949870590164193048041239
q = 275127860351348928173285174381581152299
fn = (p - 1) * (q - 1)

d = int(gmpy2.invert(e, fn))

with open('flag.enc', 'rb') as f:
    c = libnum.s2n(f.read())
print(c)

m = pow(c, d, n)
print(libnum.n2s(int(m)))
