'''
Author: Tyler96-QA 1718459369@qq.com
Date: 2023-04-08 13:03:00
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-05-09 15:56:28
FilePath: \Api_test\day6\testcase\test_login.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import pytest
import shutil
import os,sys
import allure
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'tools'))
from handle_excel import HandleExcel
from global_SystemEnv import SystemEnv
from handle_requests import public_request

"""
前置sql需要查询的表及字段如下
atfx-{}_bos_auth_users 查询语句：{'account':'#bos_user#'} 查询字段 ['passwd']
atfxgm-{}_atfx_account_info 查询语句：{'accountNumber':#account#} 查询字段：['fullName','docNo','addr','phone','email','birthDate']
atfxgm-{}_atfx_account 查询语句：{'accountNumber':#account#} 查询字段：['parentAccountNumber']
atfxgm-{}_atfx_trade_account 查询语句：{'accountNumber':#account#,'tradeAccount':'#tdaccount#'} 查询字段：['mtName','tradeAccountType','group','mtRegion','localCcy']
atfx-{}_bos_psp_control 查询语句：{'name':'cardpay','entity':'GM','gatewayType':'creditCard'} 查询字段：['charge']
渠道币种查询:
atfx-{}_bos_psp_currency 查询语句：{pspId:'cardpay'} 查询字段：['currency']
入金汇率查询：
atfxgm-{}.atfx_float_rate 查询语句：{fromCcy:'交易账号币种localCcy',toCcy:'渠道币种currency'} 查询字段：['depositRate']
"""

@pytest.mark.usefixtures('deposit_withdrawal_info')
@allure.suite('creditCard入金')
class TestCreditCard(object):

    test_data=HandleExcel(os.path.join(SystemEnv.DATA_DIR,'CP接口用例.xlsx'),'New_CreditCard_Deposit_Gm').read_excel_data_obj()

    @allure.title("cardpay入金：{case.title}")
    @pytest.mark.high
    @pytest.mark.parametrize('case',test_data)
    @pytest.mark.flaky(reruns=2, reruns_delay=2)
    @pytest.mark.run(order=0)
    def test_card_pay_deposit(self,case):
        """
        creditCard入金逻辑如下：
        根据主账号查询入金接口所需字段，从数据库获取
        根据交易账号查询交易账号币种，组别，地区等，从数据库获取
        根据交易账号币种，渠道币种，查询入金汇率。换算入金金额
        根据数据库查询的渠道手续费charge，换算入金手续费
        以上查询为每个接口提供了必传参数。入金只需提供对应测试环境的交易账号，主账号即可
        """
        setattr(SystemEnv,'depositType','cardpay')
        public_request(case)

    @allure.title("qubepay入金：{case.title}")
    @pytest.mark.high
    @pytest.mark.parametrize('case',test_data)
    @pytest.mark.flaky(reruns=2, reruns_delay=2)
    @pytest.mark.run(order=1)
    def test_qubepay_deposit(self,case):
        """
        creditCard入金逻辑如下：
        根据主账号查询入金接口所需字段，从数据库获取
        根据交易账号查询交易账号币种，组别，地区等，从数据库获取
        根据交易账号币种，渠道币种，查询入金汇率。换算入金金额
        根据数据库查询的渠道手续费charge，换算入金手续费
        以上查询为每个接口提供了必传参数。入金只需提供对应测试环境的交易账号，主账号即可
        """
        setattr(SystemEnv,'depositType','qubepay')
        public_request(case) 


    @allure.title("cashu入金：{case.title}")
    @pytest.mark.high
    @pytest.mark.parametrize('case',test_data)
    @pytest.mark.flaky(reruns=2, reruns_delay=2)
    @pytest.mark.run(order=2)
    def test_cashu_deposit(self,case):
        """
        creditCard入金逻辑如下：
        根据主账号查询入金接口所需字段，从数据库获取
        根据交易账号查询交易账号币种，组别，地区等，从数据库获取
        根据交易账号币种，渠道币种，查询入金汇率。换算入金金额
        根据数据库查询的渠道手续费charge，换算入金手续费
        以上查询为每个接口提供了必传参数。入金只需提供对应测试环境的交易账号，主账号即可
        """
        setattr(SystemEnv,'depositType','cashu')
        public_request(case) 

if __name__ == '__main__': 
    pytest.main([os.path.abspath(__file__),
                 '--count=1',
                 '--alluredir={}'.format(os.path.join(SystemEnv.REPORT_DIR,'allure_result')),
                 ])
    
    # shutil.copy2(os.path.join(SystemEnv.ROOT_PATH,'environment.xml'),os.path.join(SystemEnv.REPORT_DIR,'allure_result'))
    
    # os.system('allure generate {} -o {} --clean'.format(os.path.join(SystemEnv.REPORT_DIR,'allure_result'),
    #                                                     os.path.join(SystemEnv.REPORT_DIR,'allure_report')))

    # os.system('allure serve {}'.format(os.path.join(SystemEnv.REPORT_DIR,'allure_result')))

