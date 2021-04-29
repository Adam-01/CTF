# 赛博朋克 - zip伪加密, png LSB隐写

伪加密：  
在源数据区（50 4B 01 02）找到deCompression结构（08 00）改为（00 00），可解除伪加密。  

得到一个txt文件，用`file`识别为一张png图片，遂改后缀为png。  

PNG LSB隐写：  
用stegsolve的Data Extract，在Bit Planes框勾选RGB的第0位，且按行(row)打开，顺序为RGB，可得flag。