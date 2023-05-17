'''
Author: Tyler96-QA 1718459369@qq.com
Date: 2023-04-10 01:01:26
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-05-11 12:42:00
FilePath: \Api_test\api_framework_v1\tools\handle_extract.py
Description: 此模块用于jsonpath表达式提取接口响应数据,接口响应类型：json；并将提取的数据赋值给SystemEnv类属性作为全局变量，适用于每一个接口
'''

from jsonpath import jsonpath
from global_SystemEnv import SystemEnv
from loguru import logger
import allure
from handle_replace_mark import replace_mark_by_data

@allure.step('通过jsonpath表达式从响应结果中提取数据，并设置为全局变量')
def handleExtract(extract_str:str,resp_data:dict)->None:
    """
    从响应结果中，通过jsonpath将提取的数据设置为SystemEnv类属性，作为全局变量
    :params extract_data:jsonpath-string,从excel中读取的extract列
    :params resp_data:who extracted,接口响应数据转换成字典后提取
    """
    #将excel中读取的提取格式转换成字典
    extract_str = replace_mark_by_data(extract_str)
    extract_dict = eval(extract_str)
    with allure.step(f'需要从响应数据中提取的字段为：{list(extract_dict.keys())}'):
        logger.info(f'需要从响应数据中提取的字段为：{list(extract_dict.keys())}')
    for key,jsonpath_ in extract_dict.items():
        if isinstance(jsonpath(resp_data,jsonpath_),list): #判断是否取到了值 isinstance(对象，(类名1，类名2...))判断对象是否为类的实例
            res = jsonpath(resp_data,jsonpath_)[0]

            if isinstance(res,(str,int,float,bool)):
                setattr(SystemEnv,key,res)
                with allure.step(f'从响应数据中设置的全局变量为：{key}：{res}'):
                    logger.info(f'从响应数据中设置的全局变量为：{key}：{res}')
            elif isinstance(res,(list,tuple)):
                if len(res) != 0:
                    if isinstance(res[0],dict):
                        for keyinside,value in res[0].items():
                            setattr(SystemEnv,keyinside,value)
                            with allure.step(f'从响应数据中设置的全局变量为：{keyinside}：{value}'):
                                logger.info(f'从响应数据中设置的全局变量为：{keyinside}：{value}')
                    else:
                        setattr(SystemEnv,key,res)
                        with allure.step(f'从响应数据中设置的全局变量为：{key}：{res}'):
                            logger.info(f'从响应数据中设置的全局变量为：{key}：{res}')
                else:
                    setattr(SystemEnv,key,res)
                    with allure.step(f'从响应数据中设置的全局变量为：{key}：{res}'):
                        logger.info(f'从响应数据中设置的全局变量为：{key}：{res}')
            elif isinstance(res,dict):
                for keyinside,value in res.items():
                    setattr(SystemEnv,keyinside,value)
                    with allure.step(f'从响应数据中设置的全局变量为：{keyinside}：{value}'):
                        logger.info(f'从响应数据中设置的全局变量为：{keyinside}：{value}')
            else:
                with allure.step(f'从响应数据中设置的全局变量为：{key}：{res}'):
                    setattr(SystemEnv,key,res)
                logger.info(f'从响应数据中设置的全局变量为：{key}：{res}')
        else:
            raise AttributeError('响应提取失败')