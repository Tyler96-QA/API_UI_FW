'''
Author: Tyler96-QA 1718459369@qq.com
Date: 2023-04-08 13:03:00
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-05-07 15:59:24
FilePath: \Api_test\day6\testcase\test_login.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import shutil
from urllib.parse import urlparse
import pytest
import os,sys
import allure
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'tools'))
from handle_excel import HandleExcel
from global_SystemEnv import SystemEnv
from handle_requests import public_request


@pytest.mark.usefixtures('bos_login')
@allure.suite('GM2.0新增IB')
class TestDusuPay(object):

    test_data=HandleExcel(os.path.join(SystemEnv.DATA_DIR,'BOS接口用例.xlsx'),'new_register_bos').read_excel_data_obj()

    @allure.title("{case.title}")
    @pytest.mark.regress
    @pytest.mark.parametrize('case',test_data)
    @pytest.mark.flaky(reruns=3, reruns_delay=2) 
    def test_dusupay_deposit(self,case):
        public_request(case)


if __name__ == '__main__':  
    pytest.main([os.path.abspath(__file__),
                 ])
    
    # shutil.copy2(os.path.join(SystemEnv.ROOT_PATH,'environment.xml'),os.path.join(SystemEnv.REPORT_DIR,'allure_result'))
    
    # os.system('allure generate {} -o {} --clean'.format(os.path.join(SystemEnv.REPORT_DIR,'allure_result'),
    #                                                     os.path.join(SystemEnv.REPORT_DIR,'allure_report')))

    # os.system('allure serve {}'.format(os.path.join(SystemEnv.REPORT_DIR,'allure_result')))

