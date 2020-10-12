# 葫芦娃 - mp3stego使用

1.
```bash
cat xaa xab xac xad xae xaf xag > huluwa.mp3
```

2. 
用mp3stego解密，在mp3stego目录下  
```cmd
decode.exe -X -P GourdSmallDiamond huluwa.mp3
```
得到一个huluwa.mp3.txt文件，里面是压缩包密码。


3. 
把压缩包从huluwa.mp3中分离出来，输入刚才得到的密码，即得flag。