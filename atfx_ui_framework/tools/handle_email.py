'''
Author: Tyler96-QA 1718459369@qq.com
Date: 2023-04-04 11:12:42
LastEditors: Tyler96-QA 1718459369@qq.com
LastEditTime: 2023-04-11 00:57:17
FilePath: \Api_test\public\handle_email.py
Description: 发送邮件的模块，收发件人配置在conf目录下
'''
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from handle_config import SystemEnv

class SendEmail(object):

    def __init__(self) -> None:

        self.my_sender=SystemEnv.SENDER_163 #发送人邮箱

        self.my_pass=SystemEnv.KEY_163 #发送人授权码，登录邮箱时的验证

        self.ricever=SystemEnv.RICEVER #接收人地址

        self.sender_name=SystemEnv.SENDERNAME #发送人姓名

        self.ricever_name=SystemEnv.RICEVERNAME #接收人姓名

        self.smtp_host=SystemEnv.SMTPHOST_163 #发送邮箱SMTP服务器服务器

        self.smtp_port=int(SystemEnv.SMTPPORT) #smtp端口


    def send(self,content:any,form:str,object:str):
        """
        :param content:邮件正文
        :param form:写入格式 html/plain
        :param object:邮件主题
        """
        try:
            msg=MIMEText(content,form,'utf-8')
            msg['From']=formataddr([self.sender_name,self.my_sender])
            msg['To']=formataddr([self.ricever_name,self.ricever])
            msg['Subject']=object

            server=smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
            server.login(self.my_sender, self.my_pass)
            server.sendmail(self.my_sender,[self.ricever,],msg.as_string())
        except Exception as msg:
            print(f'请检查连接信息、格式、授权码是否正确：{msg}')
            station=False
        else:
            station=True
            server.quit()
        if station:
            print(f'邮件发送成功;sender: {self.my_sender} , reciver: {self.ricever}')

if __name__=='__main__':
    send_email=SendEmail()
    send_email.send('test','plain','testetete')
    # import os
    
    # email_list=os.listdir(os.path.join(eval(SystemEnv('ROOTPATH')),'出金邮件','withdrawalFeeReceived'))
    # for email in email_list:
    #     with open(os.path.join(eval(SystemEnv('ROOTPATH')),'出金邮件','withdrawalFeeReceived',email),'r',encoding='utf-8') as f:
    #         data=f.read()
    #     send_email.send(data,'html','第一种：withdrawalFeeReceived,ATFX: 提款请求已收到'+email.replace('.txt',':'))
    
    # email_list2=os.listdir(os.path.join(eval(SystemEnv('ROOTPATH')),'出金邮件','withdrawalReceived'))
    # for email in email_list2:
    #     with open(os.path.join(eval(SystemEnv('ROOTPATH')),'出金邮件','withdrawalReceived',email),'r',encoding='utf-8') as f:
    #         data=f.read()
    #     send_email.send(data,'html','第二种：withdrawalReceived,ATFX: 提款请求已收到'+email.replace('.txt',':'))