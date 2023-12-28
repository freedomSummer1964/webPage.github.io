# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 17:17:17 2021

@author: wenyi_zhang love tianlu_zhou
"""

import smtplib
import imaplib
import time
from datetime import datetime
from email.header import decode_header
import email
from email.mime import text
from email.utils import parseaddr


#! /usr/bin/env python3
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def get_subject(msg):
    header='11'
    for header in ['From', 'To', 'Subject']:
        value = msg.get(header, '')
        if value:
            #文章的标题有专门的处理方法
            if header == 'Subject':
                value = decode_str(value)
            else:
                value = '111'
    return value

def sendIt(sender,passwd,class_name,send_to):
    SMTPServer='smtp.163.com'
    
    message='郭闻浩 1020209029 15802210611 zhuyuanzhang110@163.com '+class_name+ ' 备注：老师，我只需要一次监考就满足四次了，所以如果分配给我的监考有多于两个的话，只需要分配给我一个就可以了~'
    # message='郭闻浩 1020209029 15802210611 zhuyuanzhang110@163.com '+class_name
    msg=text.MIMEText(message)
    msg['Subject']='监考报名'
    msg['From']=sender
    mailServer=smtplib.SMTP(SMTPServer,25)
    mailServer.login(sender,passwd)
    # mailServer.sendmail(sender,'zhangwenyi117@126.com',msg.as_string())
    mailServer.sendmail(sender,send_to,msg.as_string())
    mailServer.quit()

def guess_charest(msg):
    charset=msg.get_charset()
    if charset is None:
        content_type=msg.get('Content-Type','').lower()
        pos=content_type.find('charset=')
        if pos>=0:
            charset=content_type[pos+8:].strip()
    return charset

def txt_wrap_by(start_str, end, html):
    theBack=''
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            theBack=html[start:end].strip()
    return theBack
            
def get_content(msg):
    newsDate_return=[]
    for part in msg.walk():
        content_type = part.get_content_type()
        charset=guess_charest(part)
        if part.get_filename()!=None:
            continue
        # email_content_type=''
        content=''
        # if content_type=='text/plain':
        #     email_content_type='text'
        # elif content_type==
        if charset and content_type=='text/plain':
            try:
                content = part.get_payload(decode=True).decode(charset)
            except AttributeError:
                print('type error')
            except LookupError:
                print("unknown encoding: utf-8")
        # if email_content_type =='':
        #     print('no')
        #     #如果内容为空，也跳过
        if len(content)>0:
            theWork=content.split('|')
            theNumberOfClass=0
            for i in range(0,len(theWork)):
                if '《' in theWork[i]:
                    theClass=theWork[i]
                    theTeacher=theWork[i+1]
                    theTime=theWork[i+3]
                    newsDate_return.append([theClass,theTeacher,theTime])
                
        # newsDate=txt_wrap_by("《","》",content)
        # if newsDate!=None and len(str(newsDate))>=3:
        #     print(str(newsDate))
        #     print(str(newsDate))
            # if (str(newsDate) not in newsDate_return):
            #     newsDate_return=newsDate_return.append(str(newsDate))
    return newsDate_return

def fuckGaohong(theClass,theAnimal,theBadWeek,theBadTime):
    theValue='No'
    theTeacher=theClass[1]
    theTime=theClass[2]
    theBadDates=['5月13日']
    
    theMonthNumber=theTime.rindex('月')
    # print(theTime[1:theMonthNumber])
    if (theTime[1:theMonthNumber]!='12'):
        theTime='2022年'+theTime[1:]
    else:
        theTime='2021年'+theTime[1:]
    if (theTeacher[1:-1] not in theAnimal):
        theDateNumber=theTime.rindex('日')
        theWeek=datetime.strptime(theTime[:theDateNumber+1],'%Y年%m月%d日').weekday()
        # print(theWeek)
        if theWeek!=theBadWeek and (theBadTime not in theTime):
            theValue='Yes'
            for theBadDate in theBadDates:
                if theBadDate in theTime:
                    theValue='No'
        else:
            theValue='No'  
        
    else:
        theValue='No'
    return theValue
    

def getIt(geter, geter_password,sender,sender_password,send_to_email,theAnimal,theBadWeek,theBadTime):
    mail=imaplib.IMAP4_SSL('imap.163.com')
    mail.login(geter, geter_password)
    
    imaplib.Commands['ID']=('AUTH')
    imap_id=("name","wennie","contact",geter,"version","1.0.1","vendor","sagerKing")
    typ,dat=mail._simple_command('ID','("'+'" "'.join(imap_id)+'")')
    print(mail._untagged_response(typ,dat,'ID'))
    status,msgs=mail.select()
    
    
    mail.select("Inbox", readonly=True)
    
    result, data = mail.uid('search', None, "ALL")
    latest_email_uid = data[0].split()[-1]
    
    a=1
    while a>0:
        mail.select("Inbox", readonly=True)
        result, data = mail.uid('search', None, "ALL") # search and return uids instead
    
        if data[0].split()[-1] == latest_email_uid:
             time.sleep(0.1) # put your value here, be sure that this value is sufficient ( see @tripleee comment below)
        else:
             latest_email_uid = data[0].split()[-1]
             result, data = mail.uid('fetch',latest_email_uid, '(RFC822)') # fetch the email headers and body (RFC822) for the given ID
             msg=email.message_from_string(data[0][1].decode('gbk'))
             subject=get_subject(msg)
             if ('监考报名' in subject):
                 classes=get_content(msg)
                 # print(classes)
                 for i in range(0,len(classes)):
                     theClass=classes[i]
                     print(theClass)
                     try:
                         theValue=fuckGaohong(theClass,theAnimal,theBadWeek,theBadTime)
                     except:
                         theValue='No'
                     print(theValue)
                     if theValue=='Yes':
                         # print(1)
                         sendIt(sender,sender_password,theClass[0],send_to_email)
                 
                 print('ok!')
                 a=0
                 break
             else:
                 print('收到错误邮件-标题错误')
             

# geter='zhuyuanzhang110@163.com'
# geter_password='fcmm110402'
geter='yemenzijue@163.com'
geter_password='PXJTGHOBMBPJJZYM'
sender='zhuyuanzhang110@163.com'
sender_password='fcmm110402'
# send_to='15802210611@163.com'
send_to='tju_bba@tju.edu.cn'

theAnimal=['高宏','陆明远','李庚']
theBadWeek=3
theBadTime='13:'
getIt(geter, geter_password,sender,sender_password,send_to,theAnimal,theBadWeek,theBadTime)


# a=[[' 《会计学》 ', ' 谭庆美 ', ' 1月2日上午9:00-11:00 '], [' 《项目融资（翻转）》 ', ' 郑立群 ', ' 12月30日下午15:25-17：25 '], [' 《数据组织与管理》 ', ' 朱克珊 ', ' 12月6日上午10:25-12:00 '], [' 《商业银行经营管理》 ', ' 佘震宇 ', ' 12月29日下午15:25-17：00 '], [' 《税收理论与实务》 ', ' 梅世强 ', ' 12月4日上午：00-11:00 '], [' 《市场营销学》 ', ' 王秀宏 ', ' 12月28日下午18:00-20:00 '], [' 《工程经济学》 ', ' 王秀宏 ', ' 12月11日下午2:00-4:00 ']]
# for i in range(0,len(a)):
#     theClass=a[i]
#     theValue=fuckGaohong(theClass,theAnimal,theBadWeek,theBadTime)
#     print(theValue)
    