'''
Author: TylerQA 990687322@qq.com
Date: 2023-04-21 02:17:04
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-04-26 18:37:07
FilePath: \atfx_-ui_framework\testcases\conftest.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os,sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from driver_settings import Driver_Config
from global_SystemEnv import SystemEnv
sys.path.append(os.path.join(SystemEnv.BOS_PAGE_OBJ))
from bos_login_obj import Bos_Login

#前置：登录bos
@pytest.fixture(scope='class')
def browser():
    #打开浏览器
    browser = Driver_Config()
    bos_login = Bos_Login(browser)
    bos_login.open(SystemEnv.BOS_URL.get(SystemEnv.ENVIRONMENT))
    #登录bos
    bos_login.login_bos(SystemEnv.BOS_USER.get(SystemEnv.ENVIRONMENT).get('user'),SystemEnv.BOS_USER.get(SystemEnv.ENVIRONMENT).get('psword'))
    yield browser
    browser.quit()

@pytest.fixture()
def browser_func():
    #打开浏览器
    browser = Driver_Config()
    yield browser
    browser.quit()