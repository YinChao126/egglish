# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 15:42:26 2018

@author: YinChao
"""
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random
import re
import requests
from bs4 import BeautifulSoup


def pic_gen(url, day):
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html5lib')
    a = soup.find(property='og:image')
    a = str(a)
    obj = re.compile('(?<=content=")[^"]+')
    pic_url = obj.findall(a)
#    print(pic_url)
    if len(pic_url) > 0:
#    下载图片
        r = requests.get(pic_url[0])
        with open('raw.png', 'wb') as f:
            f.write(r.content) 
#        print(soup.select('img'),'\n\n')
    else:
        print('no picture')
        return
    
# 1.生成层叠图片 
    font_size = 160 #控制保证和目标图片保持固定比例
    
    content = 'day ' + str(day)
    l = int(len(content) / 2 + 1)
    osd_image = Image.new('RGBA',(font_size * l,font_size),(255,255,255))
    draw = ImageDraw.Draw(osd_image)
    font=ImageFont.truetype("sylfaen.ttf",size=font_size)#字体设置
    draw.text((0,0),content,(255,0,0), font = font)   
#    print('osd尺寸：',osd_image.width, osd_image.height)
#    osd_image.show()
    datas = osd_image.getdata() 
    newData = list()
    for item in datas:
        if item[0] >220 and item[1] > 220 and item[2] > 220: #此处需要完善
            newData.append(( 255, 255, 255, 0))#把非文字部分设置为透明的
        else:
            newData.append(item)
    osd_image.putdata(newData)
    
# 2.让目标图片和层叠图片融合
    img1 = Image.open( "raw.png ")
    img1 = img1.convert('RGBA')
#    print('背景图片尺寸：',img1.width, img1.height)
    r, g, b, alpha = osd_image.split()
    alpha = alpha.point(lambda i: i>0 and 60)
    img = Image.composite(osd_image, img1, alpha)
#    img.show()
    return img
    

def GetPicture(url):
#    s = '<meta property="og:image" content="https://www.washingtonpost.com/resizer/uuAjJ4Fvi2-3rd3SIHQEYPIjccg=/1484x0/arc-anglerfish-washpost-prod-washpost.s3.amazonaws.com/public/MEX3O3SCC4ZZROD7X2T27TDCEU.jpg" itemprop="image"/>'
#    print(s)
#    print('')
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html5lib')
#    a = soup.select('script')#ok
    a = soup.find(property='og:image')
#    print(a.string)
    a = str(a)
    obj = re.compile('(?<=content=")[^"]+')
    pic_url = obj.findall(a)
#    print(pic_url)
    if len(pic_url) > 0:
#    下载图片
        r = requests.get(pic_url[0])
        with open('head.jpg', 'wb') as f:
            f.write(r.content) 
        print(soup.select('img'),'\n\n')
    else:
        print('no picture')
        
def Result(day):
    '''
    生成一个字符串,然后和目标图片层叠
    目标图片固定为：raw.png
    '''
# 1.生成层叠图片 
    font_size = 160 #控制保证和目标图片保持固定比例
    
    content = 'day ' + str(day)
    l = int(len(content) / 2 + 1)
    osd_image = Image.new('RGBA',(font_size * l,font_size),(255,255,255))
    draw = ImageDraw.Draw(osd_image)
    font=ImageFont.truetype("sylfaen.ttf",size=font_size)#字体设置
    draw.text((0,0),content,(255,0,0), font = font)   
#    print('osd尺寸：',osd_image.width, osd_image.height)
#    osd_image.show()
    datas = osd_image.getdata() 
    newData = list()
    for item in datas:
        if item[0] >220 and item[1] > 220 and item[2] > 220: #此处需要完善
            newData.append(( 255, 255, 255, 0))#把非文字部分设置为透明的
        else:
            newData.append(item)
    osd_image.putdata(newData)
    
# 2.让目标图片和层叠图片融合
    img1 = Image.open( "raw.png ")
    img1 = img1.convert('RGBA')
#    print('背景图片尺寸：',img1.width, img1.height)
    r, g, b, alpha = osd_image.split()
    alpha = alpha.point(lambda i: i>0 and 60)
    img = Image.composite(osd_image, img1, alpha)
    img.show()


def getRandomColor():
    '''
    Auxiliary：不可调用
    获取一个随机颜色(r,g,b)格式的
    '''
    c1 = random.randint(0,255)
    c2 = random.randint(0,255)
    c3 = random.randint(0,255)
    return (c1,c2,c3)

if __name__ == '__main__':
    url = 'https://www.washingtonpost.com/business/economy/before-trump-putin-summit-europe-urges-china-and-us-to-halt-trade-war/2018/07/16/ccde865a-88d3-11e8-8b20-60521f27434e_story.html'
    