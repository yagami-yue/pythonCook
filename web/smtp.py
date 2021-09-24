# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:smtp.py
@time:2021/09/02
"""
# coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


class Mail:
    def __init__(self):
        # 第三方 SMTP 服务

        self.mail_host = "smtp.qq.com"  # 设置服务器:这个是qq邮箱服务器，直接复制就可以
        self.mail_pass = "onwwblsiynheddhe"  # 授权码
        self.sender = '2993907398@qq.com'  # 你的邮箱地址
        self.receivers = ['wangzichen@xmov.ai',]  # 收件人的邮箱地址，可设置为你的QQ邮箱或者其他邮箱，可多个

    def send(self):

        content = 'smtp test'  # 正文
        message = MIMEText(content, 'plain', 'utf-8')
        receivers = ','.join(self.receivers)
        message['From'] = formataddr(('yagami_yue', self.sender))
        message['To'] = formataddr(('dsdsdsdsdsds', receivers))
        subject = 'test'  # 发送的主题，可自由填写
        message['Subject'] = subject
        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)
            smtpObj.login(self.sender, self.mail_pass)
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            smtpObj.quit()
            print('邮件发送成功')
        except smtplib.SMTPException as e:
            print('邮件发送失败')


if __name__ == '__main__':
    mail = Mail()
    mail.send()
