# Reverse-it

> 题目给出一个Reverse-it文件，用脚本翻转..........

```python
with open('Reverse-it', 'rb') as f:
    with open('Reverse-it.jpg.tmp', 'wb') as fw:
        fw.write(f.read()[::-1])

with open('Reverse-it.jpg.tmp', 'rb') as f:
    with open('Reverse-it.jpg', 'wb') as fw:
        for i in range(100000):
            fw.write(bytes.fromhex(bytes.hex(f.read(1))[::-1]))
```