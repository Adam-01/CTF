# bug

1. 随便注册一个账号
![](1.jpg)

2. 找回密码
![](2.jpg)
![](3.jpg)

3. 抓包修改admin的密码
![修改admin密码](4.jpg)

4. 点manage时提示“IP Not Allowed!”，解决方法：添加HTTP Header： X-Forwarded-For: 127.0.0.1

5. 得到提示index.php?module=filemanage&do=，猜测upload

6. 通过图片马，%00截断，修改后缀名为php5，上传成功。