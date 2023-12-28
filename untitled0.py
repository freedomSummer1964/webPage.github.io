# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 09:13:26 2021

@author: 郭闻浩
"""
import time
from datetime import datetime
def txt_wrap_by(start_str, end, html):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()
def fuckGaohong(theClass,theAnimal,theBadWeek,theBadTime):
    theValue='No'
    theTeacher=theClass[1]
    theTime=theClass[2]
    
    theMonthNumber=theTime.rindex('月')

    if (theTime[1:theMonthNumber]!='12'):
        theTime='2022年'+theTime[1:]
    else:
        theTime='2021年'+theTime[1:]
    print(theTime)
    if (theTeacher[1:-1] not in theAnimal):
        theDateNumber=theTime.rindex('日')
        theWeek=datetime.strptime(theTime[:theDateNumber+1],'%Y年%m月%d日').weekday()
        print(theWeek)
        if theWeek!=theBadWeek and (theBadTime not in theTime):
            theValue='Yes'
        else:
            theValue='No'  
    else:
        theValue='No'
    return theValue
subject='fw:监考报名'
x=datetime(2021,11,29)
print(x.weekday())
# theClass=[' 《国际金融》 ', ' 王秀芹 ', ' 1月24日下午15:25-17:25 ']
# theAnimal=['高宏']
# theBadWeek=0
# theBadTime='2:00'
# value=fuckGaohong(theClass,theAnimal,theBadWeek,theBadTime)
# print(value)