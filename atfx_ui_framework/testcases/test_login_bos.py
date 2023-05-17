'''
Author: TylerQA 990687322@qq.com
Date: 2023-04-21 02:10:59
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-04-22 19:44:30
FilePath: \atfx_-ui_framework\testcases\test_login_bos.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import pytest
import sys,os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'tools'))
from global_SystemEnv import SystemEnv
sys.path.append(os.path.join(SystemEnv.BOS_PAGE_OBJ))
from bos_login_obj import Bos_Login

@pytest.mark.usefixtures('browser')
class TestLoginBos(object):

    def test_login_bos(self,browser):
        driver = Bos_Login(browser)
        driver.open('https://at-bos-frontend-sit.atfxdev.com/login')
        driver.login_bos('tyler.tang','Tl12346')

if __name__ == "__main__":
    pytest.main(['-vs',
                 os.path.abspath(__file__)])