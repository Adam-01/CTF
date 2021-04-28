# web5

## writeup

payload: ?num=1a

当num='1a'与1用==比较时，会强制类型转换成1，而num本身不是数字，因而可以通过is_numeric()

题目代码：
```php
<?php

$num = $_GET['num'];

if (!is_numeric($num)) {
    echo $num;
    if ($num == 1)
        echo 'flag{**********}';
}

?>
```