'''
Author: Tyler96-QA 1718459369@qq.com
Date: 2023-04-08 13:03:00
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-04-29 12:38:59
FilePath: \Api_test\day6\testcase\test_login.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import pytest
import os,sys
import allure
import shutil
from urllib.parse import urlparse
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'tools'))
from handle_excel import HandleExcel
from global_SystemEnv import SystemEnv
from handle_requests import public_request


@allure.suite('BOS客户名单重发邮件')
@pytest.mark.usefixtures('bos_login')
class TestBosSendEmail(object):

    test_data=HandleExcel(os.path.join(SystemEnv.DATA_DIR,'BOS接口用例.xlsx'),'重发邮件MU').read_excel_data_obj()

    @allure.title("{case.title}")
    @pytest.mark.parametrize('case',test_data)
    @pytest.mark.medium
    @pytest.mark.flaky(reruns=3, reruns_delay=2) 
    def test_bos_send_email(self,case):
        public_request(case)

if __name__ == '__main__':  
    pytest.main(['--count=5',
                 os.path.abspath(__file__),
                 '--alluredir={}'.format(os.path.join(SystemEnv.REPORT_DIR,'allure_result'))
                 ])
    
    shutil.copy2(os.path.join(SystemEnv.ROOT_PATH,'environment.xml'),os.path.join(SystemEnv.REPORT_DIR,'allure_result'))
    
    os.system('allure generate {} -o {} --clean'.format(os.path.join(SystemEnv.REPORT_DIR,'allure_result'),
                                                        os.path.join(SystemEnv.REPORT_DIR,'allure_report')))

    # os.system('allure serve {}'.format(os.path.join(SystemEnv.REPORT_DIR,'allure_result')))

