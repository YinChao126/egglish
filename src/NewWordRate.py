# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 13:25:27 2018

@author: 54206
"""

#使用方法：
#1、保证py文件和dictionary的文件路径正确
#2、直接给check_freq传一个字符串即可
#
#
#
import os
import re
import string

    

def DicCreate():
    #构建字典列表,不同的字典有不同的单词提取方法
    #partten=re.compile(r'\b[a-z]+\b')
    #AllDicFile=os.listdir(r"./dictionary/")
     
    #Gre词典   
    #GRE词典的特点是：1）每三行一个新词，第一行是单词本身，第二行是单词解释，第三行是空
    f = open(r'./dictionary/gre词汇.txt','r',encoding='UTF-8')
    lines = f.readlines()
    GreDicWords = []
    count = 1
    for line in lines:
        if (count==1):
            line=line.lower()
            GreDicWords.append(line)
            count+=1
        elif (count ==2):
            count+=1
        else:
            count =1
            
    #四六级词典
    #四六级词典的特点是：每一行只有一个单词，并且用/标注其音标
    f = open(r'./dictionary/英语四级+六级词汇大全(带音标).txt','r',encoding='UTF-16')
    lines = f.readlines()
    Cet46DicWords=[]
    for line in lines:
        if (line.find(r'/')!=-1):
            words=line.split(r'/')
            word = words[0]
            Cet46DicWords.append(word.strip())
      

    partten=re.compile(r'\b[a-z]+\b')
    partten1 = re.compile(r'\([a-zA-z]+\,[a-zA-z]+\)')
    f = open(r'./dictionary/高中英语.txt','r',encoding='UTF-8')
    lines = f.readlines()
    HignSchoolDic=[]
    for line in lines:
        if (line.find('[')!=-1):
            line = line.replace("[",' [')
            line = line.lower()
            word = re.search(partten,line).group()
            HignSchoolDic.append(word)
            word = re.search(partten1,line)
            if (word!=None):
                word = word.group()
                PastTence = word.split(',')
                HignSchoolDic.append(PastTence[0][1:])
                HignSchoolDic.append(PastTence[1][:-1])
     
    
    Dic = GreDicWords+Cet46DicWords+HignSchoolDic
    Dic = list(set(Dic))
    if ('a' not in Dic):
        Dic.append('a')
    return Dic


def check_freq(ArticalStr):
    partten=re.compile(r'[0-9]+')
    count = 0
    Dic = DicCreate()
    Articlwords=[]
    ArticalStr = ArticalStr.replace('-',' ')
    ArticalStr = ArticalStr.replace("“",' ')
    ArticalStr = ArticalStr.replace("”",' ')
    ArticalStr = ArticalStr.replace("\"",' ')
    ArticalStr = ArticalStr.replace(',',' ')
    ArticalStr = ArticalStr.replace('.',' ')
    ArticalStr = ArticalStr.replace('’',' ')
    ArticalStr = ArticalStr.replace('‘',' ')
    for word in ArticalStr.split():
        word = word.strip(string.punctuation + string.whitespace)
        if (len(word)==1):
            continue
        word = word.lower()
        if word not in Articlwords:
            if (re.match(partten,word)):
                pass
            else:
                Articlwords.append(word)
                count = count+1
    
    UnkownWord=[]
    for word in Articlwords:
        if (word not in Dic):
            UnkownWord.append(word)
            if (word[-1]=='s' or word[-1]=='y'):
                if(word[0:-1] in Dic ):
                    UnkownWord.remove(word)
                    #print (word)
            elif (word[-2:]=='ed' or word[-2:]=='er' or word[-2:]=='th' or word[-2:]=='ly'):
                if(word[0:-2] in Dic ):
                    UnkownWord.remove(word)
                    #print (word)
                elif(word[0:-1] in Dic ):
                    UnkownWord.remove(word)
                    #print (word)
            elif (word[-3:]=='ing' or word[-3:]=='man' or word[-3:]=='men' or word[-3:]=='ers'):
                if(word[0:-3] in Dic or len(word)==3):
                    UnkownWord.remove(word)
                   # print (word)
                
    #print (UnkownWord)          
    UnknowRate= len(UnkownWord)/count
    print ("生词率:%10.3f"%UnknowRate)
    return UnknowRate
    
if __name__ =='__main__':
#Dic = DicCreate()
##1、获取目录下的所有文件
#AllFile=os.listdir(r"./Article/")
##2、过滤掉非txt文件
#AllTxtFile=[]
#for file in AllFile:
#    if(file.find('.txt')!=-1):
#        AllTxtFile.append(file)
#    else:
#        pass
#    
    fin = open(r'./Article/article.txt','r')    
    lines = fin.readlines()
    Aline =""
    for line in lines:
        Aline = Aline+line
    check_freq(Aline)
    
		
        


 
        
        
    
   
    
