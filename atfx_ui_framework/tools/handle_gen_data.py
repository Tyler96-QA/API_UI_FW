'''
Author: Tyler96-QA 1718459369@qq.com
Date: 2023-04-10 22:41:45
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-04-26 19:54:54
FilePath: \Api_test\api_framework_v1\tools\handle_gen_data.py
Description: 替换excel请求数据中的占位符，函数名要与占位符一致才能成功替换
'''
import time
from faker import Faker
import uuid
from loguru import logger
from global_SystemEnv import SystemEnv
import random
from handle_database import DatabaseOperate


#实例对象作为全局变量
fake = Faker('zh-CN')
dataBase = DatabaseOperate()

#指定对外开放的类或者函数,字符串与函数的映射
__all__ = ['gen_cur_time',
           'gen_random_str',
           'gen_random_date',
           'gen_end_str',
           'gen_random_address',
           'gen_random_name',
           'gen_random_iban',
           'gen_random_swift',
           'gen_random_phone',
           'gen_random_new_phone',
           'gen_uuid',
           'gen_random_code'
           ]

def gen_cur_time()->str:
    """
    返回13位时间戳
    """
    return str(int(time.time()*1000))

def gen_random_str(min_chars=10,max_chars=12)->str:
    """
    返回10-12位随机字符串
    """
    return fake.pystr(min_chars=min_chars,max_chars=max_chars)

def gen_random_date(start_date='-30y',end_date='-18y')->str:
    """
    返回30年前至18年前的随机日期，默认格式YYYY-mm-dd
    """
    return fake.date_between(start_date=start_date,end_date=end_date).strftime('%Y-%m-%d')

def gen_end_str(suffix='TYLER')->str:
    """
    返回以指定字符结尾的大写字符串
    """
    return ''.join(fake.nic_handles(suffix=suffix)).replace('-','')

def gen_random_address()->str:
    """
    返回中国地区随机地址
    """
    return fake.address()

def gen_random_province()->str:
    """
    返回随机省份
    """
    return fake.province()
    
def gen_random_city():
    """
    返回随机城市
    """
    return fake.city_name()

def gen_random_name()->str:
    """
    返回随机firstname
    """
    return fake.name_male()

def gen_random_iban()->str:
    """
    返回随机IBAN号码
    """
    return fake.iban()

def gen_random_bankid()->str:
    """
    返回随机银行卡号
    """
    return fake.bban()

def gen_random_swift(length=11)->str:
    """
    返回随机的11位swift号码
    """
    return fake.swift(length=length)

def gen_random_phone()->str:
    """
    返回随机中国手机号码
    """
    return fake.phone_number()

def gen_random_code()->str:
    """
    返回证件号码
    """
    return fake.ssn()


def gen_uuid()->str:
    """
    返回uuid4
    """
    uuidstr = str(uuid.uuid4())
    setattr(SystemEnv,'gen_uuid',uuidstr)
    logger.info(f'生成的uuid：{uuidstr}，并设置全局变量{gen_uuid}为{uuidstr}')
    return uuidstr

#生成随机大写字符串
def gen_capitalize_str(N):
    capStr='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(random.sample(capStr,N))