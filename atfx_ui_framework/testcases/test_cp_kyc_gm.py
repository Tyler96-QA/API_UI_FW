'''
Author: TylerQA 990687322@qq.com
Date: 2023-04-23 19:30:56
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-04-26 01:38:57
FilePath: \atfx_-ui_framework\testcases\test_cp_kyc_gm.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
'''
Author: TylerQA 990687322@qq.com
Date: 2023-04-23 19:30:56
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-04-25 10:33:37
FilePath: \atfx_-ui_framework\testcases\test_cp_kyc_gm.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import pytest
import pytest_check as check
import sys,os
from loguru import logger
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'tools'))
from global_SystemEnv import SystemEnv
from handle_excel import HandleExcel
sys.path.append(os.path.join(SystemEnv.CP_PAGE_OBJ))
sys.path.append(os.path.join(SystemEnv.BOS_PAGE_OBJ))
sys.path.append(os.path.join(SystemEnv.DATA_DIR))
from gm_login_obj import Gm_Login_Obj
from bos_login_obj import Bos_Login
from bos_home_page_obj import Bos_Home_Page_Obj
from bos_clientlist_page_obj import Bos_Client_Page_Obj
from gm_home_page_obj import Gm_Home_Page_Obj
from gm_kyc_page_obj import Gm_Kyc_Obj

@pytest.mark.usefixtures('browser_func')
class TestGmKyc(object):

    test_data = HandleExcel(os.path.join(SystemEnv.DATA_DIR,'testcases.xlsx'),'gm_kyc').read_excel_data_obj()

    @pytest.mark.run(order=1)
    @pytest.mark.regress
    @pytest.mark.parametrize('data',test_data)
    @pytest.mark.dependency(depends = ['test_cp_register_gm.py::TestGmRegister::test_register_gm'], scope = 'session')
    def test_gm_kyc(self,data,browser_func):
        case_index = self.test_data.index(data)
        #runall时数据共享
        if hasattr(SystemEnv,f'account{case_index+2}'):
            data.account = getattr(SystemEnv,f'account{case_index+2}')
        if hasattr(SystemEnv,f'email{case_index+2}'):
            data.email = getattr(SystemEnv,f'email{case_index+2}')
        logger.info(f'执行用例：{data.title};kyc账号：{data.account};,邮箱：{data.email}')
        #登录页-登录CP
        LoginCP = Gm_Login_Obj(browser_func)
        LoginCP.open(SystemEnv.CP_RUL.get(SystemEnv.ENTITY).get(SystemEnv.ENVIRONMENT))
        LoginCP.login_cp_gm(data.email,data.password)

        #CP主页,识别图片验证码
        Cp_Home = Gm_Home_Page_Obj(browser_func)
        if Cp_Home.discern_email_code(data.country):

            #登录页-登录bos
            BOS_login = Bos_Login(browser_func)
            BOS_login.js_openwindows(SystemEnv.BOS_URL.get(SystemEnv.ENVIRONMENT))
            BOS_login.login_bos(SystemEnv.BOS_USER.get(SystemEnv.ENVIRONMENT).get('user'),SystemEnv.BOS_USER.get(SystemEnv.ENVIRONMENT).get('psword'),1)

            #主页-进入详情页
            BOS_Home = Bos_Home_Page_Obj(browser_func)
            BOS_Home.into_client_list(int(data.account),1)

            #详情页-获取验证码
            BOS_Client = Bos_Client_Page_Obj(browser_func)
            email_code = BOS_Client.get_email_code(2)

            #首页填写邮箱验证码完成邮箱验证
            Cp_Home.input_email_code(email_code)
        #kyc操作
        Kyc_Page = Gm_Kyc_Obj(browser_func)
        Kyc_Page.kyc_actions(data.country)
        check.is_in(Kyc_Page.success_text,'Successfully submitted personal verification information! 成功提交个人验证资料！')
        
        #触发弹窗
        Cp_Home.company_declaration()
        Cp_Home.is_under_review()

if __name__ == '__main__':  
    pytest.main(['-vs',
                 os.path.abspath(__file__),
                 '--disable-pytest-warnings'])
        

        
