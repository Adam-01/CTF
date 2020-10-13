import gmpy2
import libnum

c = 0xdc2eeeb2782c

n = 322831561921859

# yafu-x64.exe factor(322831561921859) --> p, q
p = 23781539
q = 13574881
fn = (p - 1) * (q - 1)

e = 23

d = gmpy2.invert(e, fn)

m = pow(c, d, n)

print(libnum.n2s(int(m)))

'''
s = ''
j = 0
m = hex(int(str(m)))[2:]
for i in range(len(m) // 2):
    s += chr(int(m[j:j+2], 16))
    j += 2
print(s)
'''