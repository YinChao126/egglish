# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 22:05:54 2018

@author: YinChao
"""
'''
SQL 模块使用方法：
1. 调用account_cfg(path)读取sql账户信息（严格按照host,user,passwd,database顺序）
2. 调用pymysql_connect()获取其返回值，得到连接变量
3. 调用sql_insert(table, df_data)插入记录
4. 如果有需要的话，调用sql_del_today_record()来删除记录，注意需要根据实际情况来修改sql语句
'''

import pymysql
from sqlalchemy import create_engine
import pandas as pd

global account #全局变量，用以存储用户账号信息

def account_cfg(sql_account_path):
    global account
    try:
        with open(sql_account_path, 'r') as fh:
            account = fh.readlines()
#            print(account)
    except:
        print('fail to initialize.')

def pymysql_connect():
    global account
    try:
        print("trying to connected...")
        connect = pymysql.connect(
                host = account[0].strip(),
                port = 3306,
                user = account[1].strip(),
                passwd = account[2].strip(),
                db = account[3].strip(),
                charset = "utf8"
                )
        print("connect to sql success!")
        return connect
    except:
        print('cannot connected...')
        return
    
def sql_insert(table,df):
    global account
    connect = create_engine("mysql+pymysql://"+ account[1].strip() + ":"+ account[2].strip() + "@" + account[0].strip() + ":3306/" + account[3].strip() + "?charset=utf8")
    df.to_sql(name=table,con=connect,if_exists='append',index=False,index_label=False)


def sql_del_today_record(connect, table):
    '''
    删去今天的内容,关键在于sql_delete语句，如果有特殊需求，则修改此处
    '''
    import time
    today = time.strftime("%Y-%m-%d")
    sql_delete ="delete from %s where date = \'%s\';" % (table, today)
    cur = connect.cursor()
    try:
        cur.execute(sql_delete) #像sql语句传递参数
#        results = cur.fetchall()	#获取查询的所有记录
#        print(results)
        connect.commit()#提交
    except:
        print('nothing happend')
        connect.rollback()
        return
    finally:
        connect.close()
        
###############################################################################        
if __name__ == '__main__':
    path ='sql_account.txt'
    account_cfg(path)   #首先要指定account文件的路径
    
#    header = ['date']
#    data = {'date':'2018-07-16'}      
    header = ['date','title', 'link', 'words', 'reserved']
    data = {'date':'2018-7-6','title':'test','link':'www.baidu.com',
        'words':'123','reserved':''}   
    df_data = pd.DataFrame(data,columns = header, index=[0]) #生成测试数据
    
    connect = pymysql_connect() #连接到数据库
    cur = connect.cursor()
    
    sql_del_today_record(connect,'egglish') #如果今天已经有记录，则先删除
    sql_insert('egglish',df_data) #增加今天的记录