# '''
# Author: Tyler96-QA 1718459369@qq.com
# Date: 2023-04-09 17:52:29
# LastEditors: Tyler96-QA 1718459369@qq.com
# LastEditTime: 2023-04-11 00:07:35
# FilePath: \Api_test\api_framework_v1\testcase\debug.py
# Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
# '''
# from jsonpath import jsonpath
# import os,sys
# sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'tools'))
# from handle_config import SystemEnv
# import handle_gen_data
# import re
# # dic={"access_token":"a67d3bcd-b5f4-40ea-99b5-d9416ac29aae","token_type":"bearer","refresh_token":"98df9719-4f21-468f-80c4-823ae65b4b3b","expires_in":1295999}


# # extract = '{"token":"$..access_token","expires_in":"$..expires_in"}'


# # extract_dict = eval(extract)


# # for key,jsonpath_ext in extract_dict.items():
# #     if isinstance(jsonpath(dic,jsonpath_ext),list): #判断是否取到了值 isinstance(对象，(类名1，类名2...))判断对象是否为类的实例
# #         setattr(SystemEnv,key,jsonpath(dic,jsonpath_ext)[0])
# #     else:
# #         raise AttributeError('请检查jsonpath表达式是否正确')

# # print(SystemEnv.token)
# # print(SystemEnv.__dict__)


# # add_url = 'http://mall.lemonban.com:8108/prod/prod'

# # data = {
# # 	"t": 1681095238086,
# # 	"prodName": "py58testest",
# # 	"brief": "",
# # 	"video": "",
# # 	"prodNameEn": "py58testest",
# # 	"prodNameCn": "py58testest",
# # 	"contentEn": "",
# # 	"contentCn": "<p>testeststetew33333</p>",
# # 	"briefEn": "",
# # 	"briefCn": "美白测试",
# # 	"pic": "2023/04/eb93f2a56cbb4c21893eba176a249531.png",
# # 	"imgs": "2023/04/eb93f2a56cbb4c21893eba176a249531.png",
# # 	"preSellStatus": 0,
# # 	"preSellTime": None,
# # 	"categoryId": 144,
# # 	"skuList": [{
# # 		"price": 260,
# # 		"oriPrice": 200,
# # 		"stocks": 20,
# # 		"skuScore": 1,
# # 		"properties": "",
# # 		"skuName": "",
# # 		"prodName": "",
# # 		"weight": 10,
# # 		"volume": 0,
# # 		"status": 1,
# # 		"partyCode": "55456456885666",
# # 		"prodNameCn": "py58testest",
# # 		"prodNameEn": "py58testest"
# # 	}],
# # 	"tagList": [21],
# # 	"content": "",
# # 	"deliveryTemplateId": 1,
# # 	"totalStocks": 20,
# # 	"price": 260,
# # 	"oriPrice": 200,
# # 	"deliveryModeVo": {
# # 		"hasShopDelivery": True,
# # 		"hasUserPickUp": True,
# # 		"hasCityDelivery": True
# # 	}
# # }

# # login_url = 'http://mall.lemonban.com:8108/adminLogin'
# # login_data = {"principal":"student","credentials":"123456a","imageCode":"lemon"}

# # header = {'locale':'zh-CN'}
# # import requests

# # login_resp = requests.request('post',login_url,json=login_data)


# # header['Authorization'] = 'bearer'+login_resp.json().get('access_token')


# # add_resp = requests.request('post',add_url,json=data,headers=header)

# # print(add_resp.text)
# # {'result':'2023/04/2bc4f3840b774e3188105c8d295ea57c.png'}


# # import time
# # print(int(time.time()*1000))

# # from faker import Faker

# # fake=Faker('zh-CN')


# # print(fake.prefix())


# """
# 只匹配一个字符
# \d  只匹配0-9的数字
# \w 匹配数字字母下划线,0-9a-zA-Z_
# . 除了换行符(\n)以外的所有字符

# 数量匹配
# * 匹配前一个字符，0次或者多次
# + 匹配前一个字符，一次或者多次
# ？ 匹配前一个字符，0次或者一次

# """
# strr = """
# {
#  "t": #cur_time#,
#  "prodName": "py57测试#random_str#",
#  "brief": "",
#  "video": "",
#  "prodNameEn": "py57test#random_str#",
#  "prodNameCn": "py57测试#random_str#",
#  "contentEn": "",
#  "contentCn": "<p>testeststetew33333</p>",
#  "briefEn": "",
#  "briefCn": "美白测试",
#  "pic": #pic_path#,
#  "imgs": #pic_path#,
#  "preSellStatus": 0,
#  "preSellTime": null,
#  "categoryId": 144,
#  "skuList": [{
#   "price": 260,
#   "oriPrice": 200,
#   "stocks": 20,
#   "skuScore": 1,
#   "properties": "",
#   "skuName": "",
#   "prodName": "",
#   "weight": 10,
#   "volume": 0,
#   "status": 1,
#   "partyCode": "#cur_time#",
#   "prodNameCn": "py57test#random_str#",
#   "prodNameEn": "py57test#random_str#"
#  }],
#  "tagList": [21],
#  "content": "",
#  "deliveryTemplateId": 1,
#  "totalStocks": 20,
#  "price": 260,
#  "oriPrice": 200,
#  "deliveryModeVo": {
#   "hasShopDelivery": true,
#   "hasUserPickUp": true,
#   "hasCityDelivery": false
#  }
# }
# """

# #findall(规则，字符串)，在字符串中从头到尾去匹配，只要符合要求就会拿出来
# paran = r'#(\w+)#'
# to_be_replaced_mark = list(set(re.findall(paran,strr)))

# SystemEnv.pic_path = 'helloword.png'
# # cur_time = int(time.time()*1000)
# # random_str = faker.Faker('zh-CN').pystr(min_chars=8,max_chars=10)
# # SystemEnv.pic_path = 'jiodjoioihohhhioh.png'
# # # for mark in to_be_replaced_mark:
# #     if mark == 'cur_time':
# #         #用变量cur_time的值替换字符串当中的{cur_time}
# #         strr = strr.replace(f'#{mark}#',str(cur_time))

# #     elif mark == 'random_str':
# #         strr = strr.replace(f'#{mark}#',str(random_str))

# #     else:
# #         strr = strr.replace(f'#{mark}#',getattr(SystemEnv,mark))

# # print(strr)

# from handle_config import SystemEnv
# import handle_gen_data
# for mark in to_be_replaced_mark:
#     if hasattr(SystemEnv,mark):
#         strr = strr.replace(f'#{mark}#',str(getattr(SystemEnv,mark)))
#     else:
#         if mark in handle_gen_data.__all__:
#             strr = strr.replace(f'#{mark}#',getattr(handle_gen_data,mark)())

# print(strr)
# import json
# import os
# import base64
# from handle_config import SystemEnv
# with open(os.path.join(SystemEnv.ROOT_PATH,'imgs','address.png'),'rb') as f:
#     re = f.read()

# import handle_gen_data
# from handle_database import DatabaseOperate
# from handle_config import SystemEnv
# import handle_gen_data

# phone = handle_gen_data.random_phone()

# #发送验证码
# send_url = 'http://mall.lemonban.com:8107/user/sendRegisterSms'
# method = 'put'
# # data = 
# from handle_replace_mark import replace_mark_by_data
# dataBase = DatabaseOperate()
# sql = "SELECT mobile_code FROM tz_sms_log WHERE user_phone='15098012462'"
# data = dataBase.search_in_mysql(mysql='MYSQL',sql=sql)

# for key,value in data.items():
#     setattr(SystemEnv,key,value)

# print(SystemEnv.mobile_code)
# # print(dict(a=2))

# a=1.8899
# print('%.2f'%a)
# li = [1,2,3,4]
# def func2(a,b,c,d):
#     print(a,b,c,d)
# func2(*li)

# def func(user,host,password,port,b):
#     print(host,user,password,port,b)

# MYSQL = {
#     'host' : '47.113.180.81',
#     'user' : 'lemon',
#     'password' : 'lemon123',
#     'port' : 3306
# }

# func(**MYSQL,b='我解包以外的参数')

# def func2(a,b):
#     print(a,b)

# func2(*li)
# import pytest,os
# def test_assume():
# 	pytest.assume(1 == 2)
# 	print("断言失败会继续执行代码")
	
# if __name__ == '__main__':
#     pytest.main(['-vs',
#                  os.path.abspath(__file__)])
# from datetime import datetime, timedelta
# a="2023-04-21T11:27:36.241Z"
# b=a.replace('T',' ').replace('Z','')[:-4]

# sime1 = datetime.strptime(b,'%Y-%m-%d %H:%M:%S')
# print(sime1)
# uptime = sime1+timedelta(hours=8,seconds=0,milliseconds=0)
# print(uptime)
# #importing datetime module for now()  
# from datetime import datetime, timedelta  
  
# # using now() to get present_time  
# present_time ='{:%H:%M:%S}'.format( datetime.now())    

   
# print("Present time at greenwich meridian is ",
#        end = "")  
# print( present_time )
  
# updated_time = datetime.now() + timedelta(hours=6)
# print( updated_time )
#!/usr/bin/env python3
#!coding:utf-8
# import re
# a = '#(.+)#'
# d = '#rend_phone#'
# c = "#'email'#"

# print(eval(re.findall(a,c)[0]))
# # c = a+str(index)
# setattr(SystemEnv,a+str(index),'1111111')
# # print(getattr(SystemEnv,'token1'))
# a = """{
# 	'data': {
# 		'code': 1004,
# 		'message': 'success',
# 		'data': {
# 			'token': {
# 				'access_token': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNvS0tiaFZOZmNyVlVTdlNWbmZjdy15ZTU2eEZ1YUlLYURNcTR3M2xRVEEifQ.eyJqdGkiOiJsa2cwWHYxWWhCTHg0NzNVQlhKbDIiLCJzdWIiOiJmMDlmNDdiZC00Y2NiLTRlZTUtYWIyMi1lYzRiNjIwYzE2ODUiLCJpc3MiOiJodHRwczovL2F0LWlkcC1zaXQuYXRmeGRldi5jb20iLCJpYXQiOjE2ODI3NTU1NDksImV4cCI6MTY4Mjc1OTE0OSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBwaG9uZSBudCBhZGRyZXNzIGVudGl0eSBlbmNyeXB0X3NlY3JldCIsImF1ZCI6ImJvcyJ9.G-LCHiN-aZZqh9YYiiq5wcBrrc1RcUPJgwEeHAiCKsRcgYPz0TBTRw7B8e9QV-Siox6TebAx_hwLxElOVXgIa2Ll0zpzTjxDHxuxk1BVBuCOuPAuw0-knU-lRKS3Pq6-5o-772NVvrdKUUzvOjGJu4aVDGm3qaPY2QJQQQkeuOruPimyVxo0vsynMXy3AH4cthTzq7ftKRD7MyGWemISf6CVOHEXNa3u-yQrYZQ7Zdh0YkahLYiAMam22To7oecL21vtDdAP2u9dE7RaCHPN_EzeETLV_5KjLL3Qv9xSeC7HIktSmWCw4dih2uZPQzYJ6kz6TgmXFkaufwWJPGVbdg',
# 				'id_token': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNvS0tiaFZOZmNyVlVTdlNWbmZjdy15ZTU2eEZ1YUlLYURNcTR3M2xRVEEifQ.eyJzdWIiOiJmMDlmNDdiZC00Y2NiLTRlZTUtYWIyMi1lYzRiNjIwYzE2ODUiLCJuYW1lIjoidHlsZXIgdGVzdCIsImVtYWlsIjoidHlsZXIudGFuZ0A2MzE3LmlvIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBob25lX251bWJlciI6IjgyMTg2OTYxNjU0NjUiLCJwaG9uZV9udW1iZXJfdmVyaWZpZWQiOmZhbHNlLCJyb2xlcyI6W10sImN1c3RvbSI6eyJkZXZpY2VfaWQiOiIiLCJhY2NvdW50TnVtYmVyIjoxMDAwMDA1MzQ5fSwiZW50aXR5IjoiR00iLCJlbmNyeXB0X3NlY3JldCI6IkN6T01sZzJ4dGdDMFVta1JQZHBpK1E9PSIsIm5vbmNlIjoiIiwiYXRfaGFzaCI6IiIsInNpZCI6IiIsImF1ZCI6ImJvcyIsImV4cCI6MTY4Mjc1OTE1MCwiaWF0IjoxNjgyNzU1NTUwLCJpc3MiOiJodHRwczovL2F0LWlkcC1zaXQuYXRmeGRldi5jb20ifQ.mha5FuHeYFUibbdVTmj94jobmgLLYW5JXm3YrzS0uGvqzCzTypgSHFoKiMtdm4xnEgaRqf-GtZqbaqXXcc33WvdQcKu88JiT05FknkWp_dyA62o5u4G8kycIFsfyoKpC1qJ37yifnlSWf3o2SU0-AhEpPBr4dX9-If0Snz7QN9hZRthVnqa_h_g2guymD0Td2fAxxTsOWcUg_8uYX4XTnapHnzRiu9wODsZx7j3p31QTYPTdPJ-ntS61NWGQUAGIYCodxY5oycZFmsARCr7WMs2esb4oSG2fvKIzHLkxqkRundEYUvOtEtbSGqdlwffhUpiR4c_4m75-AtAqWbiZtA',
# 				'expires_in': 3600,
# 				'token_type': 'Bearer'
# 			},
# 			'cpHomeUrl': 'https://at-client-portal-sit.atfxdev.com'
# 		}
# 	},
# 	'statusCode': 200,
# 	'message': 'Success'
# }"""

# {"bankRefNo":"$..bankRefNo","_id":"$.._id","lastUpdateDate":"$..lastUpdateDate","createDate_mt":"$..createDate_mt","createDate":"$..createDate","ID":"$..ID","creditCardDepositID":"$..creditCardDepositID","accountNumber":"$..accountNumber","tradeAccount":"$..tradeAccount","currStatus":"$..currStatus","createDomain":"$..createDomain"}


#生成一个字典





















