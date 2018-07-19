# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 16:00:25 2018

@author: YinChao
"""

import sql
import get_article
import picture_generator
import time
import pandas as pd
import webbrowser

###############################################################################
# API接口列表：
'''
>> Run(pattern) 自动运行，可以智能判断是否完成了翻译。
如果没有开始翻译：完成初始化配置与资源准备（生成out文件夹，合成图片，生成原文和译文，打开网页）
如果完成了翻译：则自动将资源整合到万能页，做成微信文章，等待用户发朋友圈（需要等待审核）

>> ReTry(pattern) 重新运行（与Run功能一致，但是可以覆盖今天的记录）
'''

# 模块内的系统函数（不可被调用）
'''
Init(pattern) 初始化，pattern为正则表达式，用来筛选感兴趣的内容
RunTranslator() 直接运行,选择感兴趣的文章，翻译完毕后自动生成输出资料
RunReport() 生成微信文章，提交到万能页上，等待发送
'''
###############################################################################
article_dic = []
global days #今天是第几天打卡
global today_path #今天输出的path

#days = 0
def Init(search_re):   
    '''
    1. 连接上数据库，查看今天是第几天打卡
    2. 打开华盛顿邮报主页，过滤掉一部分链接
    3. 返回可用的文章列表参数给后续应用端
    '''
    global days
    
    import os
    try:
        today = time.strftime("%Y-%m-%d")
        today_path = '../out/' + today
#        print(today_path)
        os.mkdir(today_path)
    except:
        pass
    
    path ='../config/sql_account.txt'
    sql.account_cfg(path)   #首先要指定account文件的路径
    connect = sql.pymysql_connect() #连接到数据库
#    sql.sql_del_today_record(connect,'egglish') #如果今天已经有记录，则先删除
    cur = connect.cursor()
    sql_delete ="select * from egglish;"
    try:
        cur.execute(sql_delete) 
        results = cur.fetchall()	
        days = len(results) + 1#获取查询的记录,今天是第n+1天
#        print(days)
    except: #第一次建立数据库
        days = 1
    
    '''
    打开华盛顿邮报的主页，并过滤不适合以及不感兴趣的链接
    '''
    main_dic = get_article.get_washingtonpost_link()
    '''
    此处要加入生词统计的逻辑
    '''
    dic = get_article.ArticleFilter(main_dic, search_re) #筛选文章
#    article_dic = dic
    return dic

def RunTranslator(article_dic):
    '''
    1. 显示感兴趣的链接，并等待用户输入序号
    2. 自动创建输出文件夹，并创建原文文档、译文文档、合成图片
    3. 自动打开浏览器，用户自行翻译并记录在译文文档上
    '''
    global days
    global today_path
    
    print('run translator func')
    
    i = 0
    for s in article_dic:
        print(i, ':', s['name'], '\n')  
        i += 1
    index = input('witch one do you like?') #手动选择感兴趣的文章
    
    url = article_dic[int(index)]['link']
    title = article_dic[int(index)]['name']
#    print(url)
    
    #1. 生成out/day文件夹、生成原文文档、译文文档、合成图片
    import os
    try:
        today = time.strftime("%Y-%m-%d")
        today_path = '../out/' + today
#        print(today_path)
        os.mkdir(today_path)
    except:
        pass
    #此处生成原文文档
    content = title + '\n\n' #title
    content += get_article.GetArticle(url) #content
    content += '\n\n' + url + '\n' #url
#    print(content)
    trans_file_name = today_path + '/source.txt'  
    with open(trans_file_name, 'w', encoding = 'utf-8') as fh:
#        fh.writelines('原文：')
        fh.write(content)
    
    #此处生成译文文档（空白）
    trans_file_name = today_path + '/trans.txt'    
    with open(trans_file_name, 'w', encoding = 'utf-8') as fh:
        fh.writelines('译文：\n')
    
    #提交今天的信息到数据库上
    header = ['day', 'date','title', 'link', 'words', 'reserved']
    data = {'day':days, 'date':today,'title':title,'link':url,
        'words':'123','reserved':''}   
    df_data = pd.DataFrame(data,columns = header, index=[0]) #生成测试数据
    connect = sql.pymysql_connect() #连接到数据库
    sql.sql_del_today_record(connect,'egglish') #如果今天已经有记录，则先删除
    sql.sql_insert('egglish',df_data) #增加今天的记录
    #合成图片    
    img = picture_generator.pic_gen(url, days) #生成图片
    pic_name = today_path + '/pic.jpg'
    img.save(pic_name)
    
    #打开网址，用户开始翻译
    webbrowser.open(article_dic[int(index)]['link']) #打开网页


def RunReport():
    '''
    自动整合输出文档并打开浏览器生成待推送的微信文章
    '''
    print('run report func')
    
def Run(re_pattern):
#    import os
#    try:
#        today = time.strftime("%Y-%m-%d")
#        today_path = '../out/' + today
##        print(today_path)
#        os.mkdir(today_path)
#    except:
#        pass
    try: #如果文件夹已经创建，则判断译文是否完成，如果完成，则直接提交report。否则重做
        today = time.strftime("%Y-%m-%d")
        today_path = '../out/' + today
        trans_file_name = today_path + '/trans.txt'
        with open(trans_file_name, 'r', encoding = 'utf-8') as fh:
            content = fh.read()
        if len(content) > 10:
            RunReport()
        else:
#            connect = sql.pymysql_connect() #连接到数据库
#            sql.sql_del_today_record(connect,'egglish') #如果今天已经有记录，则先删除
            dic = Init(re_pattern)
            RunTranslator(dic)
    except: #如果没有创建文件夹，则重做
        dic = Init(re_pattern)
        RunTranslator(dic)
        

def ReTry(re_pattern):
    dic = Init(re_pattern)
#    print(dic)
    RunTranslator(dic)
    
###############################################################################
# 辅助函数
###############################################################################


#if __name__ == '__main__':
#    print('hi')
    
#    data = {
#        "code": code,   #此处只接受单个数据吗？
#        "date": date,
#        "opens":today_open,
#        "high":today_high,
#        "low":today_low,
#        "close":cur_price,
#        "ratio":ratio,
#        "amount":amount,
#        "vol":vol
#        } #创建一个空的dataframe
##    print(data)
##    df = pd.DataFrame(data)
#    df = pd.DataFrame(data,columns=['code','date','opens','high','low',
#                             'close','ratio','amount','vol'],index=[0])
#    df_to_mysql(con, 'daily_report', df_data)
#    df_data.to_sql()
#    df_data.to_sql(name='daily_report',con=con,if_exists='append',index=False,index_label=False)
 
#def mkdir(path):
#    '''
#    生成文件夹,压根儿没那么麻烦好嘛？
#    直接 os.mkdir()即可
#    '''
#    import os
#    path=path.strip()# 去除尾部 \ 符号
#    path=path.rstrip("\\")
#    isExists=os.path.exists(path)
#    if not isExists:
#        os.makedirs(path) 
#        print( path+' 创建成功')
#        return True
#    else:
#        print( path+' 目录已存在')
#        return False
