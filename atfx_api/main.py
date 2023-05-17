'''
Author: Tyler96-QA 1718459369@qq.com
Date: 2023-04-08 17:15:21
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-04-29 16:50:12
FilePath: \Api_test\api_framework_v1\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import pytest
import os,sys
from loguru import logger
import datetime
import shutil
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'tools'))
from global_SystemEnv import SystemEnv


#写入日志文件中
log_file = os.path.join(SystemEnv.LOG_DIR,'log-{}.log'.format(datetime.datetime.now().strftime('%Y-%m-%d')))
logger.add(log_file,
           rotation='5 MB',#每个日志文件的大写
           retention=10, #最多存储10个日志
           encoding='utf-8' #日志文件编码
           )


pytest.main(['-m','high',
             '--alluredir={}'.format(os.path.join(SystemEnv.REPORT_DIR,'allure_result')),
             '--count=1'])

shutil.copy2(os.path.join(SystemEnv.ROOT_PATH,'environment.xml'),os.path.join(SystemEnv.REPORT_DIR,'allure_result'))

os.system('allure generate {} -o {} --clean'.format(os.path.join(SystemEnv.REPORT_DIR,'allure_result'),
                                                    os.path.join(SystemEnv.REPORT_DIR,'allure_report')))

os.system('allure serve {}'.format(os.path.join(SystemEnv.REPORT_DIR,'allure_result')))