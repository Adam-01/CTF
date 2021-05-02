# No one knows regex better than me - preg_match()反斜杠转义

正则中的pattern中的反斜杠\会先在字符串转义，再在正则中转义。

payload:
`?zero=ZmxhZw==&first=a||||.php`

题目代码：
```php
 <?php 
error_reporting(0);
$zero = $_REQUEST['zero'];
$first = $_REQUEST['first'];
$second = $zero.$first;
if (preg_match_all("/Yeedo|wants|a|girl|friend|or|a|flag/i", $second)) {
    $key = $second;
    if (preg_match("/\.\.|flag/", $key)) {
        die("Noooood hacker!");
    }else{
        $third = $first;
        if (preg_match("/\\|\056\160\150\x70/i", $third)) {     # 注：这里\\|会发生两次转义（字符串先转义，正则再转义），使得字符|成为普通字符；\056等数字匹配相应的ascii字符
            $end = substr($third, 5);
            highlight_file(base64_decode($zero).$end); //maybe flag in flag.php
        }
    }
}
else{
    highlight_file(__FILE__);
}
```