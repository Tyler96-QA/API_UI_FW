'''
Author: TylerQA 990687322@qq.com
Date: 2023-04-26 16:27:38
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-04-27 11:44:21
FilePath: \atfx_-ui_framework\testcases\test_review.py
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
from bos_home_page_obj import Bos_Home_Page_Obj
from bos_clientlist_page_obj import Bos_Client_Page_Obj


@pytest.mark.usefixtures('browser')
class TestReview(object):

    test_data = HandleExcel(os.path.join(SystemEnv.DATA_DIR,'testcases.xlsx'),'gm_kyc').read_excel_data_obj()
    
    @pytest.mark.run(order=2)
    @pytest.mark.regress
    @pytest.mark.parametrize('data',test_data)
    def test_review(self,data,browser):
        case_index = self.test_data.index(data)
        if hasattr(SystemEnv,f'account{case_index+2}'):
            data.account = getattr(SystemEnv,f'account{case_index+2}')

        logger.info(f'当前用例：审核主账号： {data.account}')

        #进入账号详情页
        bos_home = Bos_Home_Page_Obj(browser)
        bos_home.into_client_list(data.account)

        #审核
        bos_client_list = Bos_Client_Page_Obj(browser)
        bos_client_list.review(data.account,1)

        #断言并获取交易账号
        check.is_in(bos_client_list.status,'Successful (1st Review) 成功(初审)')

if __name__ == '__main__':  
    pytest.main(['-vs',
                 os.path.abspath(__file__),
                 '--disable-pytest-warnings'])    
