# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 16:32:15 2018

@author: 54206
"""

import os
import re
import string
  #高中英语
partten1=re.compile(r'\b[a-z]+\b')
partten = re.compile(r'\([a-zA-z]+\,[a-zA-z]+\)')
f = open(r'./dictionary/高中英语.txt','r',encoding='UTF-8')
lines = f.readlines()
HignSchoolDic=[]

for line in lines:
    if (line.find('[')!=-1):
        line = line.lower()
        word = re.search(partten,line)
        if (word != None):
            word = word.group()
            print (word)
 


