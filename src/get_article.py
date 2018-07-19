# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 15:37:01 2018

@author: YinChao
"""


import re
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import webbrowser

###############################################################################
def get_washingtonpost_link():
    '''
    从华盛顿邮报的主页上爬取文章名和链接地址
    缺陷：还不能根据自己的兴趣进行选择（如sport/business)
    '''
    url = 'https://www.washingtonpost.com/?noredirect=on'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}
    html = ''
    try:
        response = requests.get(url,headers = headers)                  
    #    response.encoding = 'utf-8'                        #解决中文乱码
        if response.status_code == 200:                     #判断是否爬取网页成功
            html = response.text
        else:
            print('web busy')
            return
    except RequestException:
        print('cannot open this web')
        return 
    soup = BeautifulSoup(html,'html5lib')    
    l = soup.select('a')
#    print(l)
#    title_name = []
#    web_link = []
    dic = []   # {'name' : 'link'}
    for link in l:
        t = link.get('title')#获取title
        s = link.get('href') #获取链接地址
        if t != None:
#            print(link, '\n')
#            title_name.append(t)
#            web_link.append(s)
            dic.append({'name':t, 'link':s})
#            print(t)
#            print(link.get('href'))
#            print('')
    return dic


###############################################################################

#a = get_washingtonpost_link()
#for s in a:
#    print(s['name'])
#    print('')
    
###############################################################################    
#print(a[-1])
def GetArticle(url):
    '''
    根据指定url网址，获取文章的内容
    '''
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}
    try:
        response = requests.get(url,headers = headers)                  
    #    response.encoding = 'utf-8'                        #解决中文乱码
        if response.status_code == 200:                     #判断是否爬取网页成功
            html = response.text
        else:
            print('web busy')
    #        return
    except RequestException:
        print('cannot open this web')
    soup = BeautifulSoup(html,'html5lib')  
    l = soup.select('p') #获取段落p
    
    article = '  '
    for link in l:
        s = link.get_text()
        article += s
        article += '\n  '
    return article
def ArticleFilter(dic, pattern):
    '''
    将主页获取的字典列表进行筛选，剔除不感兴趣和看不懂的项目
    根据标题，初步判断是否感兴趣
    根据打开的内容，结合四六级/GRE的词汇量，判断文章难度，太难了删掉
    
    dic 原始列表
    pattern 正则表达式
    '''
    dic_left = []
    
    for item in dic:
        # 1. 正则表达式删去不感兴趣的
        obj = re.compile(pattern)
        match = obj.findall(item['name'])
        try:
            trash = match[0]
            dic_left.append(item)
            # 2. Get Article排除太难的，太长的文章
    #        content = GetArticle(item['link'])
        except:
            pass
    return dic_left

def TranslatorRun(dic):
    i = 0
    for s in dic:
        print(i, ':', s['name'], '\n')  
        i += 1
    index = input('witch one do you like?') #手动选择感兴趣的文章
    webbrowser.open(dic[int(index)]['link']) #打开网页
    file = open('today.txt','w')
    file.write('say something...')
    file.close()

############################################################################### 
############################################################################### 
    
#def GetPicture(url):
#    s = '<meta property="og:image" content="https://www.washingtonpost.com/resizer/uuAjJ4Fvi2-3rd3SIHQEYPIjccg=/1484x0/arc-anglerfish-washpost-prod-washpost.s3.amazonaws.com/public/MEX3O3SCC4ZZROD7X2T27TDCEU.jpg" itemprop="image"/>'
##    print(s)
##    print('')
#    res = requests.get(url)
#    soup = BeautifulSoup(res.text,'html5lib')
##    a = soup.select('script')#ok
#    a = soup.find(property='og:image')
##    print(a.string)
#    a = str(a)
#    obj = re.compile('(?<=content=")[^"]+')
#    pic_url = obj.findall(a)
##    print(pic_url)
#    if len(pic_url) > 0:
##    下载图片
#        r = requests.get(pic_url[0])
#        with open('head.jpg', 'wb') as f:
#            f.write(r.content) 
#        print(soup.select('img'),'\n\n')
#    else:
#        print('no picture')
#
#from PIL import Image, ImageDraw, ImageFont, ImageFilter
##import random
#def PictureHandle(pic_in):
#    '''
#    对一个图片进行编辑，层叠自定义内容
#    '''
#    img1 = Image.open( "raw.png ")
#    img1 = img1.convert('RGBA')
##    img1.show()
#    
#    img2 = Image.open( "osd.jpg ")
#    img2 = img2.convert('RGBA')
#    
#    
#    img2 = img2.resize((1484, 1025))
##    img2.show()
#      
#    r, g, b, alpha = img2.split()
#    alpha = alpha.point(lambda i: i>0 and 204)
# 
#    img = Image.composite(img2, img1, alpha)
#    img.show()
#    img.save( "blend2.png")
##    img.show()
##    img.save( "blend.png")
#
##    target.save('out.png')  # 保存图片
#    
#import random
#def Verify():
#    '''
#    生成5位数的验证码,没啥用
#    '''
#    code = []
#    width = 150  ##生成的图片宽度
#    height = 60  ###生成的图片高度
#    bgcolor = (255,255,255)   ##生成的图片背景色,白色
#    img = Image.new('RGB',(width,height),bgcolor)  ##生成图片
#    draw = ImageDraw.Draw(img)
#    while True:
#        s = random.randint(48,90)
#        if s>57 and s<65:
#            continue
#        else:
#            code.append(chr(s))
# 
#            if len(code)==5:
#                break 
#    print(code)
#    draw.text( (random.randint(10, 20),random.randint(0, 5)),
#               code[0],
#               (10,7,100),
#               font = ImageFont.truetype('simsun.ttc',random.randint(35,50))  )
#    draw.text( (random.randint(25, 40),random.randint(0, 5)),
#               code[1],
#               (10,7,100),
#               font = ImageFont.truetype('simsun.ttc',random.randint(35,50))  )
#    draw.text( (random.randint(45, 60),random.randint(0, 5)),
#               code[2],
#               (10,7,100),
#               font = ImageFont.truetype('simsun.ttc',random.randint(35,50))  )
#    draw.text( (random.randint(65, 80),random.randint(0, 5)),
#               code[3],
#               (10,7,100),
#               font = ImageFont.truetype('simsun.ttc',random.randint(35,50))  )
#    draw.text( (random.randint(85, 100),random.randint(0, 5)),
#               code[4],
#               (10,7,100),
#               font = ImageFont.truetype('simsun.ttc',random.randint(35,50))  )
#    params = [1 - float(random.randint(1, 2)) / 100,
#              0.1,
#              0.8,
#              0,
#              1 - float(random.randint(1, 10)) / 100,
#              float(random.randint(1, 2)) / 500,
#              0.001,
#              float(random.randint(1, 2)) / 500
#              ]
#  
#    img = img.transform((150,60), Image.PERSPECTIVE, params)
#    img.show()
#    
##------------------------------------------------------------------------------
#from PIL import Image
#from PIL import ImageDraw
#from PIL import ImageFont
#import random
# 
#def getRandomColor():
#    '''
#    Auxiliary：不可调用
#    获取一个随机颜色(r,g,b)格式的
#    '''
#    c1 = random.randint(0,255)
#    c2 = random.randint(0,255)
#    c3 = random.randint(0,255)
#    return (c1,c2,c3)
# 
#def CreateOsd(day):
#    '''
#    Auxiliary：不可调用
#    生成一个用于层叠的字符串
#    '''
#    content = 'day ' + str(day)
#    # 获取一个Image对象，参数分别是RGB模式。宽150，高30，随机颜色
#    image = Image.new('RGBA',(100*4,62),(255,255,255))
#    #image.show()
#    # 获取一个画笔对象，将图片对象传过去
#    draw = ImageDraw.Draw(image)
#    # 
#    #！！！！字体目录：C:\Windows\WinSxS
#    ## 获取一个font字体对象参数是ttf的字体文件的目录，以及字体的大小
#    font=ImageFont.truetype("sylfaen.ttf",size=62)
#    ## 在图片上写东西,参数是：定位，字符串，颜色，字体
#    draw.text((0,0),content,(0,0,0), font = font)  
#    image.show()
#    image.save(open('test.png','wb'),'png')
#    
#    
#def Result(day):
#    '''
#    生成一个字符串,然后和目标图片层叠
#    目标图片固定为：raw.png
#    '''
## 1.生成层叠图片 
#    font_size = 160 #控制保证和目标图片保持固定比例
#    
#    content = 'day ' + str(day)
#    l = int(len(content) / 2 + 1)
#    osd_image = Image.new('RGBA',(font_size * l,font_size),(255,255,255))
#    draw = ImageDraw.Draw(osd_image)
#    font=ImageFont.truetype("sylfaen.ttf",size=font_size)#字体设置
#    draw.text((0,0),content,(255,0,0), font = font)   
#    print('osd尺寸：',osd_image.width, osd_image.height)
##    osd_image.show()
#    datas = osd_image.getdata() 
#    newData = list()
#    for item in datas:
#        if item[0] >220 and item[1] > 220 and item[2] > 220: #此处需要完善
#            newData.append(( 255, 255, 255, 0))#把非文字部分设置为透明的
#        else:
#            newData.append(item)
#    osd_image.putdata(newData)
#    
## 2.让目标图片和层叠图片融合
#    img1 = Image.open( "raw.png ")
#    img1 = img1.convert('RGBA')
#    print('背景图片尺寸：',img1.width, img1.height)
#    r, g, b, alpha = osd_image.split()
#    alpha = alpha.point(lambda i: i>0 and 60)
#    img = Image.composite(osd_image, img1, alpha)
#    img.show()
    

###############################################################################
#a = get_washingtonpost_link() #从主页上获取原始文章列表
#a_left = ArticleFilter(a, 'Trump')
##Translator(a_left)       
#GetPicture(a_left[11]['link'])
#PictureHandle('head.jpg')


#Verify()    
#getRandomColor()

#CreateOsd(2)
#Result(12)

if __name__ == '__main__':
    url = 'https://www.washingtonpost.com/business/economy/before-trump-putin-summit-europe-urges-china-and-us-to-halt-trade-war/2018/07/16/ccde865a-88d3-11e8-8b20-60521f27434e_story.html'
    content = GetArticle(url)
    with open('test.txt', 'w', encoding = 'utf-8') as fh:
        fh.write(content)
