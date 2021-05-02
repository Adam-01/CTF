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
        if (preg_match("/\\|\056\160\150\x70/i", $third)) {
            $end = substr($third, 5);
            highlight_file(base64_decode($zero).$end);//maybe flag in flag.php
        }
    }
}
else{
    highlight_file(__FILE__);
}