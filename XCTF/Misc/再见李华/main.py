import hashlib
import sys

charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

for a in charset:
    for b in charset:
        for c in charset:
            for d in charset:
                for e in charset:
                    for f in charset:
                        flag = (a + b + c + d + e + f).encode()
                        part_md5 = hashlib.md5(flag).hexdigest()[0:16] 
                        print(flag)
                        if part_md5 == b'1a4fb3fb5ee12307':
                            print('found: ' + flag)
                            sys.exit()