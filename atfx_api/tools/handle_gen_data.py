'''
Author: Tyler96-QA 1718459369@qq.com
Date: 2023-04-10 22:41:45
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-05-09 15:08:20
FilePath: \Api_test\api_framework_v1\tools\handle_gen_data.py
Description: 替换excel请求数据中的占位符，函数名要与占位符一致才能成功替换,相见https://blog.csdn.net/wt2337493578/article/details/127054353
'''
import time
from faker import Faker
import uuid
from loguru import logger
from global_SystemEnv import SystemEnv
import random
from handle_database import DatabaseOperate
from datetime import datetime, timedelta
from urllib.parse import urlparse


#实例对象作为全局变量
fake = Faker('zh-CN')
dataBase = DatabaseOperate()

#指定对外开放的类或者函数,字符串与函数的映射
__all__ = ['gen_cur_time',
           'gen_random_str',
           'gen_random_date',
           'gen_end_str',
           'gen_ramdom_address',
           'gen_random_name',
           'gen_random_iban',
           'gen_random_swift',
           'gen_random_phone',
           'gen_random_new_phone',
           'gen_uuid',
           'gen_deposit_amount',
           'createDate_updata'
           'lastUpdateDate_updata',
           'gen_random_new_email',
           'origin_cp',
           'origin_bos',
           'gen_charge',
           'gen_idcode',
           'gen_random_postcode',
           'gen_withdrawal_amount'
           ]

def gen_cur_time()->str:
    """
    返回13位时间戳
    """
    logger.info('执行gen_cur_time方法来替换占位符')
    return str(int(time.time()*1000))

def gen_random_str(min_chars=10,max_chars=12)->str:
    """
    返回10-12位随机字符串
    """
    logger.info('执行gen_random_str方法来替换占位符')
    return fake.pystr(min_chars=min_chars,max_chars=max_chars)

def gen_random_date(start_date='-30y',end_date='-18y')->str:
    """
    返回30年前至18年前的随机日期，默认格式YYYY-mm-dd
    """
    logger.info('执行gen_random_date方法来替换占位符')
    return fake.date_between(start_date=start_date,end_date=end_date).strftime('%Y-%m-%d')

def gen_end_str(suffix='TYLER')->str:
    """
    返回以指定字符结尾的大写字符串
    """
    logger.info('执行gen_end_str方法来替换占位符')
    return ''.join(fake.nic_handles(suffix=suffix)).replace('-','')

def gen_ramdom_address()->str:
    """
    返回中国地区随机地址
    """
    logger.info('执行gen_ramdom_address方法来替换占位符')
    return fake.address()

def gen_random_postcode():
    """
    返回随机邮编
    """
    logger.info('执行gen_random_postcode方法来替换占位符')
    return fake.postcode()

def gen_random_name()->str:
    """
    返回随机firstname
    """
    logger.info('执行gen_random_name方法来替换占位符')
    return fake.name_male()

def gen_random_iban()->str:
    """
    返回随机IBAN号码
    """
    logger.info('执行gen_random_iban方法来替换占位符')
    return fake.iban()

def gen_random_swift(length=11)->str:
    """
    返回随机的11位swift号码
    """
    logger.info('执行gen_random_swift方法来替换占位符')
    return fake.swift(length=length)

def gen_random_phone()->str:
    """
    返回随机中国手机号码
    """
    logger.info('执行gen_random_phone方法来替换占位符')
    return fake.phone_number()

def gen_random_new_phone()->str:
    """
    返回数据库没有记录的手机号
    """
    logger.info('执行gen_random_new_phone方法来替换占位符')
    while True:
        new_phone = fake.phone_number()
        logger.info(f'使用faker随机生成手机号：{new_phone}')
        logger.info('查询数据库该手机号是否注册')
        sql = f'SELECT * FROM tz_user WHERE user_mobile="{new_phone}"'
        data = dataBase.search_in_mysql(mysql='MYSQL',sql=sql,many=3)
        if data:
            logger.info('手机号{}已注册，重新生成手机号查询数据库是否已注册')
        else:
            logger.info(f'手机号{new_phone}未注册')
            logger.info(f'设置全局变量 new_phone：{new_phone}')
            SystemEnv.new_phone = new_phone
            return new_phone

def gen_idcode():
    """
    返回中国地区身份证号码
    """
    logger.info('执行gen_idcode方法来替换占位符')
    return fake.ssn()

def gen_uuid()->str:
    """
    返回uuid4
    """
    logger.info('执行gen_uuid方法来替换占位符')
    uuidstr = str(uuid.uuid4())
    setattr(SystemEnv,'gen_uuid',uuidstr)
    logger.info(f'生成的uuid：{uuidstr}，并设置全局变量{gen_uuid}为{uuidstr}')
    return uuidstr


def gen_deposit_amount()->str:
    """
    返回入金金额和手续费
    """
    logger.info('执行gen_deposit_amount方法来替换占位符')
    ran_amount = random.randint(20,800)
    logger.info(f'设置全局变量入金金额为：amount：{ran_amount}')
    setattr(SystemEnv,'amount',str(ran_amount))
    #根据渠道汇率换算入金金额
    channel_amount = '%.0f'%(float('%.4f'%SystemEnv.depositRate)*ran_amount)
    logger.info(f'设置全局变量渠道入金金额：channel_amount：{channel_amount}')
    setattr(SystemEnv,'channel_amount',str(channel_amount))
    
    if SystemEnv.charge:
    #换算手续费
        fee = '%.2f'%(ran_amount*SystemEnv.charge/100)
    else:
        fee = '%.2f'%0.00
    logger.info(f'设置全局变量fee：{fee}')
    setattr(SystemEnv,'fee',str(fee))

    return str(channel_amount)

def gen_withdrawal_amount()->str:
    """
    返回随机出金金额，0<,>交易账号余额
    """
    withdrawal_amount = random.randint(1,int(SystemEnv.balance))
    logger.info('执行gen_withdrawal_amount方法来替换占位符')
    logger.info(f'设置全局变量withdrawal_amount：{withdrawal_amount}')
    setattr(SystemEnv,'withdrawal_amount',withdrawal_amount)
    return str(withdrawal_amount)


def gen_charge()->str:
    if SystemEnv.charge:
        return str('%.2f'%SystemEnv.charge)+'%'
    else:
        return '0.00%'


def createDate_updata()->str:
    """
    将数据库时间转换成当地时间
    """
    logger.info('执行createDate_updata方法来替换占位符')
    creat_time = SystemEnv.createDate.replace('T',' ').replace('Z','')[:-4]
    uptime = datetime.strptime(creat_time,'%Y-%m-%d %H:%M:%S')+timedelta(hours=8,seconds=0,milliseconds=0)
    return datetime.strftime(uptime,'%Y-%m-%d %H:%M:%S')

def lastUpdateDate_updata():
    """
    将数据库时间转换成当地时间
    """
    logger.info('执行lastUpdateDate_updata方法来替换占位符')
    creat_time = SystemEnv.lastUpdateDate.replace('T',' ').replace('Z','')[:-4]
    uptime = datetime.strptime(creat_time,'%Y-%m-%d %H:%M:%S')+timedelta(hours=8,seconds=0,milliseconds=0)
    return datetime.strftime(uptime,'%Y-%m-%d %H:%M:%S')

def gen_random_new_email():
    """
    生成随机邮箱，并查询数据库邮箱是否已注册
    """
    while True:
        new_emali = fake.company_email()
        email_data = dataBase.search_in_mongodb(SystemEnv.MONGODB.get('uri'),
                                                'atclientpoolsit',
                                                'usersmu',
                                                {'email': new_emali})
        if not email_data:
            break
    logger.info(f'返回数据库atclientpoolsit中usersmu未注册的随机邮箱，并设置为全局变量：email:{new_emali}')
    setattr(SystemEnv,'email',new_emali)
    return new_emali

def origin_cp():
    """
    CP接口请求头origin参数
    """
    return urlparse(SystemEnv.CP_URL.get(SystemEnv.ENTITY).get(SystemEnv.ENVIRONMENT)).hostname

def origin_bos():
    """
    BOS接口请求体origin参数
    """
    return urlparse(SystemEnv.BOS_URL.get(SystemEnv.ENTITY).get(SystemEnv.ENVIRONMENT)).hostname