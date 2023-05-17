'''
Author: TylerQA 990687322@qq.com
Date: 2023-04-21 02:10:59
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-04-26 01:14:12
FilePath: \atfx_-ui_framework\testcases\test_login_bos.py
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
sys.path.append(os.path.join(SystemEnv.DATA_DIR))
from gm_register_obj import Gm_Register_Page_Obj
from gm_home_page_obj import Gm_Home_Page_Obj

#读取测试文件
handle_data = HandleExcel(os.path.join(SystemEnv.DATA_DIR,'testcases.xlsx'),'gm_register')

@pytest.mark.usefixtures('browser_func')
class TestGmRegister(object):

    test_data = handle_data.read_excel_data_obj()
    
    @pytest.mark.dependency()
    @pytest.mark.regress
    @pytest.mark.run(order=0)
    @pytest.mark.parametrize('data',test_data)
    def test_register_gm(self,browser_func,data):
        logger.info(f'当前用例：{data.title}')
        case_index = self.test_data.index(data)

        Register = Gm_Register_Page_Obj(browser_func)
        Register.open(data.url)
        #页面弹窗
        Register.is_limit_exist()
        #页面语言
        Register.chose_lang()
        #填写注册表单
        Register.fill_register_form(data.livecountry,data.name,data.sruname,data.phone,data.email,data.password,case_index+2,data.inv_code)
        
        #断言
        Home = Gm_Home_Page_Obj(browser_func)
        account = Home.get_account()
        logger.info(f'注册成功：{Home.account_txt}')
        check.is_in('ID',Home.account_txt)
        setattr(SystemEnv,f'account{case_index+2}',account)

        #保存测试数据到下一个流程
        kyc_data = HandleExcel(os.path.join(SystemEnv.DATA_DIR,'testcases.xlsx'),'gm_kyc')
        kyc_data.sava_excel_data('B',case_index+2,99999)
        kyc_data.sava_excel_data('B',case_index+2,account)
        kyc_data.sava_excel_data('D',case_index+2,data.password)
        

if __name__ == "__main__":
    pytest.main(['-vs',
                 os.path.abspath(__file__)])