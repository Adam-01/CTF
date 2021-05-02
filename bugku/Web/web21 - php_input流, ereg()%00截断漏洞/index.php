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