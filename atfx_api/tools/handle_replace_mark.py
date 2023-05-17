'''
Author: Tyler96-QA 1718459369@qq.com
Date: 2023-04-11 00:48:27
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-04-27 19:25:21
FilePath: \Api_test\api_framework_v1\tools\handle_replace_mark.py
Description:替换excel中的占位符
'''
import re
from global_SystemEnv import SystemEnv
import handle_gen_data 
from loguru import logger
import allure


@allure.step('判断是否需要对字符串进行替换操作，将#key#替换成真实的值')
def replace_mark_by_data(req_str:str,pattern:str='#(\w+)#')->str:
    """
    根据正则表达式提取字符串并返回非重列表
    :param req_str:被提取的字符串
    :param pattern:匹配规则：正则表达式，默认为'#(\w+)#'
    """
    mark_list = re.findall(pattern,req_str)
    if mark_list:
        with allure.step('字符串中有要替换的mark,从全局变量或者内置方法中替换mark'):
            logger.info('字符串中有要替换的mark')
        to_be_replaced_mark = sorted(list(set(mark_list)),key=mark_list.index) #去重列表并不打乱原有的排序
        logger.info(f'需要替换的mark：{to_be_replaced_mark}')
        for mark in to_be_replaced_mark:#遍历mark，判断全局变量SystemEnv是否有mark属性
            if hasattr(SystemEnv,mark): #判断全局变量SystemEnv有mark属性，就替换
                global_data = str(getattr(SystemEnv,mark))
                logger.info(f"从全局变量类的属性中获取值来替换字符串中的mark：将 #{mark}# 替换为{global_data}")
                with allure.step(f"从全局变量类的属性中获取值来替换字符串中的mark：将 #{mark}# 替换为{global_data}"):
                    req_str = req_str.replace(f'#{mark}#',global_data)
            else:#全局变量SystemEnv没有mark属性，调用handle_gen_data模块方法返回值替换 
                    func_data = getattr(handle_gen_data,mark)()
                    logger.info(f"从python方法返回的值来替换字符串中的mark：将 #{mark}# 替换为{func_data}")
                    with allure.step(f"从全局变量类的属性中获取值来替换字符串中的mark：将 #{mark}# 替换为{func_data}"):
                        req_str = req_str.replace(f'#{mark}#',func_data)
    else:
        with allure.step("字符串中没有要替换的mark"):
            logger.info('字符串中没有要替换的mark')
    
    with allure.step(f'返回的字符串为str：\n{req_str}'):
        logger.info(f'返回的字符串为str：\n{req_str}')
        return req_str #返回替换后的字符串