from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from django.conf import settings
import random
import string
import time
import io


class GenPic:
    def __init__(self):
        # 将字体文件放置于static文件内，不依赖于系统
        self.font_path = '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf'
        # 设置验证码的位数
        self.number = 4
        # 生成验证码图片的高度和宽度，可以依据实际情况选择
        self.size = (90, 38)
        # 背景颜色，默认为白色
        self.bgcolor = (255, 255, 255)
        # 字体颜色，默认为蓝色
        self.fontcolor = (0, 0, 255)
        # 干扰线颜色。默认为红色
        self.linecolor = (255, 0, 0)
        # 是否要加入干扰线
        self.draw_line = True
        # 加入干扰线条数的上下限
        self.line_number = (1, 5)
        # 上传文件展示路径前缀
        static_base = '/'
        static_url = settings.MEDIA_URL


    # 获取随机字串作为验证码
    def gen_text(self):
        source = list(string.ascii_letters)
        for item in range(0, 10):
            source.append(str(item))
        # number是生成验证码的位数
        return ''.join(random.sample(source, self.number))


    # 用来绘制干扰线
    def gene_line(self, draw, width, height):
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill=self.linecolor)


    def gene_code(self, request):
        # save_path = settings.MEDIA_ROOT + "/"
        # filename = int(time.time())
        width, height = self.size  # 宽和高
        # 创建图片
        image = Image.new('RGBA', (width, height), self.bgcolor)
        # 验证码的字体和字体大小
        font = ImageFont.truetype(self.font_path, 25)
        # 创建画笔
        draw = ImageDraw.Draw(image)
        # 生成字符串，得到随机数字与字母组合
        text = GenPic.gen_text(self)
        # print(text)
        # 将得到的字符串保存到session
        request.session['vk'] = text
        # 设置5分钟过期
        request.session.set_expiry(5 * 60)
        font_width, font_height = font.getsize(text)
        # 字符串写到图片上
        draw.text(
            ((width - font_width) / self.number,
            (height - font_height) / self.number),
            text, font=font, fill=self.fontcolor)  # 填充字符串

        # 调用画笔的point()函数绘制噪点
        for i in range(0, 100):
            xy = (random.randrange(0, width), random.randrange(0, height))
            fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
            draw.point(xy, fill=fill)

        # 绘制干扰线段
        if self.draw_line:
            GenPic.gene_line(self, draw, width, height)
            GenPic.gene_line(self, draw, width, height)
            GenPic.gene_line(self, draw, width, height)
            GenPic.gene_line(self, draw, width, height)
        image = image.transform((width + 20, height + 10), Image.AFFINE, (1, -0.3, 0, -0.1, 1, 0), Image.BILINEAR)  # 创建扭曲
        # 滤镜，边界加强
        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        # 释放画笔
        del draw
        # 将图片保存然后返回给用户
        #image.save('%s%s.png' % (save_path, filename))  # 保存验证码图片
        #image_data = open(save_path + str(filename) + '.png', "rb").read()
        # return HttpResponse(image_data, content_type="image/png")
        
        # 直接内存文件操作，将图片数据返回，不用担心验证码图片过多
        buf = io.BytesIO()
        # 将图片保存在内存中，文件类型为png
        image.save(buf, 'png')
        # 将内存中的图片数据返回给客户端，MIME类型为图片png
        # return HttpResponse(buf.getvalue(), 'image/png')
        return text, buf.getvalue()
