'''
Author: Tyler96-QA 1718459369@qq.com
Date: 2023-04-08 13:03:00
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-05-09 19:55:32
FilePath: \Api_test\day6\testcase\test_login.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import pytest
import os,sys
import allure
import shutil
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'tools'))
from handle_excel import HandleExcel
from global_SystemEnv import SystemEnv
from handle_requests import public_request

"""
前置sql需要查询的表及字段如下
atfx-{}_bos_auth_users 查询语句：{'account':'#bos_user#'} 查询字段 ['passwd']
atfxgm-{}_atfx_account_info 查询语句：{'accountNumber':#account#} 查询字段：['fullName','email','lang','country']
atfxgm-{}_atfx_account 查询语句：{'accountNumber':#account#} 查询字段：['accType']
"""

@pytest.mark.usefixtures('deposit_withdrawal_info')
@pytest.mark.usefixtures('from_bos_to_cp_get_token')
@allure.suite('电子钱包出金')
class TestEWalletWithdrawal(object):

    test_data=HandleExcel(os.path.join(SystemEnv.DATA_DIR,'CP接口用例.xlsx'),'New_Ewallet_Withdrawal_Gm').read_excel_data_obj()

    @allure.title("Neteller出金{case.title}")
    @pytest.mark.high
    @pytest.mark.parametrize('case',test_data)
    @pytest.mark.flaky(reruns=2, reruns_delay=2)
    @pytest.mark.run(order=7)
    def test_neteller_withdrawal(self,case):
        """
        出金逻辑如下：
        通过接口查询交易账号余额，判断余额是否为0，为0跳过用例
        通过接口查询交易账号是否存在未处理的出金，存在则跳过用例
        接口查询该账号是否存在Neteller出金方式，不存在则跳过用例
        以上条件都满足，出金。BOS转成功。断言出金接口返回数据
        """
        setattr(SystemEnv,'eWalletName','Neteller')
        if hasattr(SystemEnv,'balance') and SystemEnv.balance < 1:
            pytest.skip('交易账号余额为0跳过用例')
        elif hasattr(SystemEnv,'exist') and SystemEnv.exist == True:
            pytest.skip('交易有未处理的出金请求，跳过用例')
        elif hasattr(SystemEnv,'Neteller') and SystemEnv.Neteller == []:
            pytest.skip('不存在Neteller出金方式，跳过用例')
        else:
            public_request(case)


    @allure.title("Skrill出金：{case.title}")
    @pytest.mark.high
    @pytest.mark.parametrize('case',test_data)
    @pytest.mark.flaky(reruns=2, reruns_delay=2)
    @pytest.mark.run(order=8)
    def test_skrill_withdrawal(self,case):
        """
        出金逻辑如下：
        通过接口查询交易账号余额，判断余额是否为0，为0跳过用例
        通过接口查询交易账号是否存在未处理的出金，存在则跳过用例
        接口查询该账号是否存在Skrill出金方式，不存在则跳过用例
        以上条件都满足，出金。BOS转成功。断言出金接口返回数据
        """
        setattr(SystemEnv,'eWalletName','Skrill')
        if hasattr(SystemEnv,'balance') and SystemEnv.balance < 1:
            pytest.skip('交易账号余额为0跳过用例')
        elif hasattr(SystemEnv,'exist') and SystemEnv.exist == True:
            pytest.skip('交易有未处理的出金请求，跳过用例')
        elif hasattr(SystemEnv,'Skrill') and SystemEnv.Skrill == []:
            pytest.skip('不存在Skrill出金方式，跳过用例')
        else:
            public_request(case)

    
    @allure.title("CashU出金：{case.title}")
    @pytest.mark.high
    @pytest.mark.parametrize('case',test_data)
    @pytest.mark.flaky(reruns=2, reruns_delay=2)
    @pytest.mark.run(order=9)
    def test_cashu_withdrawal(self,case):
        """
        出金逻辑如下：
        通过接口查询交易账号余额，判断余额是否为0，为0跳过用例
        通过接口查询交易账号是否存在未处理的出金，存在则跳过用例
        接口查询该账号是否存在Skrill出金方式，不存在则跳过用例
        以上条件都满足，出金。BOS转成功。断言出金接口返回数据
        """
        setattr(SystemEnv,'eWalletName','CashU')
        if hasattr(SystemEnv,'balance') and SystemEnv.balance < 1:
            pytest.skip('交易账号余额为0跳过用例')
        elif hasattr(SystemEnv,'exist') and SystemEnv.exist == True:
            pytest.skip('交易有未处理的出金请求，跳过用例')
        elif hasattr(SystemEnv,'CashU') and SystemEnv.CashU == []:
            pytest.skip('不存在CashU出金方式，跳过用例')
        else:
            public_request(case)

if __name__ == '__main__':

    pytest.main([os.path.abspath(__file__),
                 '--count=1',
                 '--alluredir={}'.format(os.path.join(SystemEnv.REPORT_DIR,'allure_result'))
                 ])
    
    # shutil.copy2(os.path.join(SystemEnv.ROOT_PATH,'environment.xml'),os.path.join(SystemEnv.REPORT_DIR,'allure_result'))
    
    # os.system('allure generate {} -o {} --clean'.format(os.path.join(SystemEnv.REPORT_DIR,'allure_result'),
    #                                                     os.path.join(SystemEnv.REPORT_DIR,'allure_report')))

    # os.system('allure serve {}'.format(os.path.join(SystemEnv.REPORT_DIR,'allure_result')))

