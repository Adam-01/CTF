# Get-the-key.txt

附件forensic100，用`file`查看
```
# file forensic100
forensic100: Linux rev 1.0 ext2 filesystem data, UUID=0b92a753-7ec9-4b20-8c0b-79c1fa140869
```

挂载：
```bash
mount forensic100 some/dir/
```

进入挂载目录，解压文件名为1的文件，就是flag  