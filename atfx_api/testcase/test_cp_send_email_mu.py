'''
Author: Tyler96-QA 1718459369@qq.com
Date: 2023-04-08 13:03:00
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-04-29 16:44:41
FilePath: \Api_test\day6\testcase\test_login.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from urllib.parse import urlparse
import pytest
import os,sys
import allure
import shutil
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'tools'))
from handle_excel import HandleExcel
from global_SystemEnv import SystemEnv
from handle_requests import public_request

@allure.suite('会员中心设置页面改密发送邮箱')
class TestCpSendEmail(object):

    test_data=HandleExcel(os.path.join(SystemEnv.DATA_DIR,'CP接口用例.xlsx'),'改密发送邮件_Mu').read_excel_data_obj()

    @allure.title("{case.title}")
    @pytest.mark.parametrize('case',test_data)
    @pytest.mark.flaky(reruns=3, reruns_delay=2) 
    @pytest.mark.medium
    def test_cp_send_email(self,case):
        public_request(case)

if __name__ == '__main__':  
    pytest.main(['--count=1',
                 os.path.abspath(__file__),
                 '--alluredir={}'.format(os.path.join(SystemEnv.REPORT_DIR,'allure_result'))
                 ])
    
    shutil.copy2(os.path.join(SystemEnv.ROOT_PATH,'environment.xml'),os.path.join(SystemEnv.REPORT_DIR,'allure_result'))
    
    os.system('allure generate {} -o {} --clean'.format(os.path.join(SystemEnv.REPORT_DIR,'allure_result'),
                                                        os.path.join(SystemEnv.REPORT_DIR,'allure_report')))

    # os.system('allure serve {}'.format(os.path.join(SystemEnv.REPORT_DIR,'allure_result')))

