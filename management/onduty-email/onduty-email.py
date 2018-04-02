#!/usr/bin/env python
#coding: utf-8

import smtplib
import email
from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
import datetime
import time
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.template.loader import render_to_string



from random import Random  # 用于生成随机码
from django.core.mail import send_mail  # 发送邮件模块
from django.core.mail import EmailMessage

#TODO to be finished
mail_host = "xxxxx"
mail_user = "xxxxx"
mail_pwd = "xxxxx"
mail_postfix = "xxxxx"

def sendmail(to_list,subject,content):
  # translation
    me = mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEMultipart('related')
    msg['Subject'] = email.Header.Header(subject,'utf-8')
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    msg.preamble = 'This is a multi-part message in MIME format.'
    msgAlternative = MIMEMultipart('alternative')
    msgText = MIMEText(content, 'plain', 'utf-8')
    msgAlternative.attach(msgText)
    msg.attach(msgAlternative)
    try:
        s = smtplib.SMTP_SSL()
        s.connect(mail_host, 587)
        s.login(mail_user,mail_pwd)
        s.sendmail(me, to_list, msg.as_string())
        s.quit()
    except Exception,e:
        print e
        return False
    return True

def sendhtmlmail(to_list,subject,content):
  # translation
    me = mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEMultipart('related')
    msg['Subject'] = email.Header.Header(subject,'utf-8')
    msg['From'] = mail_user
    msg['To'] = ";".join(to_list)
    msg.preamble = 'This is a multi-part message in MIME format.'
    msgAlternative = MIMEMultipart('alternative')
    msgText = MIMEText(content, 'html', 'utf-8')
    msgAlternative.attach(msgText)
    msg.attach(msgAlternative)
    try:
        print dir(smtplib)
        s = smtplib.SMTP()
        s.connect(mail_host, 587)
        s.ehlo()
        s.starttls()
        s.login(mail_user,mail_pwd)
        s.sendmail(mail_user, to_list, msg.as_string())
        s.quit()
    except Exception,e:
        print e
        return False
    return True

if __name__ == '__main__':
    candidate_list = ["AAA(aaa)",
                      "BBB(bbb)",
                      "CCC(ccc)"]
    to_list = [
                #RD
                "aaa.net",
                "bbb.net",
                "ccc.net"
                ]

    delta = 6
    first_day = datetime.datetime.strptime("20171204", "%Y%m%d")
    today = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d")
    #today = datetime.datetime.strptime(("2017-12-24"), "%Y-%m-%d")
    that_day = today + datetime.timedelta(days = delta)
    week_iter_1 = ((today - first_day).days / 7) % len(candidate_list)
    week_iter_2 = (week_iter_1 + 1) % len(candidate_list)

    title = "本周(" + today.strftime("%Y%m%d") + "-" + that_day.strftime("%Y%m%d") + ")服务端值周安排"
    detail = "<br> 日期: " + today.strftime("%Y-%m-%d") + " -> " + that_day.strftime("%Y-%m-%d") + "<br \> " + \
    """
      <br>    服务端值周同学:
    """ + \
    candidate_list[week_iter_1] + ", " + candidate_list[week_iter_2] + "<br \><br>相关报警及case请及时跟进.<br \>"
    if sendhtmlmail(to_list,title, detail):
        print "Success!"
    else:
        print "Fail!"