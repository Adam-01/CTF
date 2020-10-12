# exif隐写2

1. 打开属性，发现base64解码得flagisnohere

2. 用`exiftool(-k).exe exif.jpg`检查图片exif信息，发现两个base64，解码得flag。