import gmpy2

p = 473398607161
q = 4511491
e = 17

fn = (p - 1) * (q - 1)
d = gmpy2.invert(e, fn)
print(d)