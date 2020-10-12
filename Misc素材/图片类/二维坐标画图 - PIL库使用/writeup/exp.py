# 从paintpaintpaint.jpg中提取出一个很长的字符串形式的十六进制字符串到coordinate.data

with open('coordinate.data', 'r') as f:
    data = f.read()

# 把以字符串形式表示的十六进制，转换为bytes（二进制）类型，写入文件
s = b''
j = 0
with open('coordinate.txt', 'wb') as f:
    for i in range(len(data) // 2):
        s += bytes.fromhex(data[j:j+2])
        j += 2
    f.write(s)  

# 绘图
import PIL
from PIL import Image

with open('coordinate.txt', 'r') as f:
    coordinates = f.read().split()

# 创建图像，颜色模式RGB，大小512x512，底色白色
img = PIL.Image.new('RGB', (512, 512), (255, 255, 255))
            #     颜色模式   图片大小       图片底色

# 根据坐标画像素
for co in coordinates:
    co = co[1:-1].split(',')
    img.putpixel((int(co[1]), int(co[0])), (0, 0, 0))
            #      纵坐标        横坐标        颜色

img.show()
img.save('flag.png')