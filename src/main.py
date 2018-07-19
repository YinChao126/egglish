# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 15:36:27 2018

@author: YinChao
"""
import sql
import egglish_api as egglish
import pandas as pd
'''
main函数使用示例：
直接调用run即可（自动判断是否完成了翻译）
如果需要重新来，则调用ReTry即可
'''
###############################################################################
#dic = egglish.Init('')
#egglish.RunTranslator(dic)
egglish.Run('Trump')