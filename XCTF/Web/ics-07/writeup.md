# isc-07

OS：Linux

关键函数
```php
if(preg_match('/.+\.ph(p[3457]?|t|tml)$/i', $filename)){
    die("Bad file extension");
```

绕过：$filename = 1.php/.