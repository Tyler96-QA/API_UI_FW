'''
Author: Tyler96-QA 1718459369@qq.com
Date: 2023-04-01 22:39:33
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-04-18 12:12:51
FilePath: \Full_stack\python_full_stack\public\handle_log.py
Description: 日志输出。日志收集器、控制台、文本输出Level配置在config文件中
'''

import logging
import datetime
import logging
import os
import sys
from global_SystemEnv import SystemEnv


class MyLog(object):
    """
    日志模块。调用此模块时会默认在上级和上上级目录下新建一个log文件用于存储log
    """
    
    def __new__(cls,name:str=SystemEnv.LOGGERNAME) -> object:#返回一个对象

        """
        调用此模块时会默认在上级和上上级目录下新建一个log文件用于存储log
        :param name:日志收集器名称
        """
        #在当前运行文件的父级目录下新建一个log目录用于存储log.log文件
        Log_path=os.path.join(os.path.dirname(os.path.dirname(sys._getframe().f_back.f_code.co_filename)),'log')
        if not os.path.exists(Log_path):
            os.mkdir(Log_path)

        #创建一个自己的日志收集器
        my_logger=logging.getLogger(name)
        #设置收集器收集的日志等级
        my_logger.setLevel(SystemEnv.LOGGERLEVEL.upper())

        #创建一个输出渠道，输出到控制台
        sh_log=logging.StreamHandler()
        #设置输出到控制台渠道的日志级别
        sh_log.setLevel(SystemEnv.STREAMLEVEL.upper())

        #创建一个输出渠道，输出到文件中,设置编码格式，中文也可输出,文件名以当前时间区分
        fh_log=logging.FileHandler(os.path.join(Log_path,'log-{}.log'.format(datetime.datetime.now().strftime('%Y-%m-%d'))),encoding='utf-8')
        #设置输出到文件渠道的日志级别
        fh_log.setLevel(SystemEnv.FILELEVEL.upper())


        #将输出渠道添加进收集器中
        my_logger.addHandler(sh_log)
        my_logger.addHandler(fh_log)

        #日志输出格式
        formater = '%(name)s - %(asctime)s - %(module)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s'
        fm_log=logging.Formatter(formater)
        #设置渠道输出格式
        sh_log.setFormatter(fm_log)
        fh_log.setFormatter(fm_log)

        return my_logger

if __name__=='__main__':
    my_log=MyLog()
    my_log.info('test')
    from global_SystemEnv import SystemEnv
    from handle_excel import HandleExcel
    fun = getattr(HandleExcel(os.path.join(SystemEnv.DATA_DIR,'后端接口用例.xlsx'),'上传文件接口v2'),'read_excel_data_obj')
    print(fun)
