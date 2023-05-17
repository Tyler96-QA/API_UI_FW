'''
Author: Tyler96-QA 1718459369@qq.com
Date: 2023-04-02 21:50:19
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-04-18 12:10:27
FilePath: \Full_stack\python_full_stack\public\handle_config.py
Description: 定义一个全局变量类，所有的环境变量都是这个类的属性，调用这个类即可访问所有属性
'''

import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import conf


#反射所有环境变量并赋值给对象的属性
class Environment(object):

    def __new__(cls) -> any:
        for item in dir(conf):
            if not item.startswith("__") and not item.endswith("__") and not type(item).__name__ == 'module':
                setattr(cls,item,getattr(conf,item))
        
        return cls
        
SystemEnv=Environment() #实例化全局变量内，import实例对象SystemEnv即拥有conf中的全局变量。每一个用例模块导入的都是一个初始化的拥有conf配置文件数据的SystemEnv对象，而不会被其他用例模块赋值的全局变量影响
