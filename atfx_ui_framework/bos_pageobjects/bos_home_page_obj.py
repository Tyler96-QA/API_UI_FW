'''
Author: TylerQA 990687322@qq.com
Date: 2023-04-21 01:56:16
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-04-26 19:17:05
FilePath: \atfx_-ui_framework\pageobjects\bos_login_obj.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import sys,os,time
from loguru import logger
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'tools'))
from global_SystemEnv import SystemEnv
sys.path.append(os.path.join(SystemEnv.BOS_PAGELOCS_DIR))
from basepage import BasePage
from bos_home_page_locs import Bos_Home_Page_Locs as home_los


class Bos_Home_Page_Obj(BasePage):

    #展开客户名单页面
    def into_client_list(self,account,winindex=0):
        self.switch_windows(winindex,'切换到BOS首页窗口')
        time.sleep(1)
        #判断客户管理导航栏是否已展开
        client_open_ele = self.get_attribute(home_los.client_management_open,'class','判断客户管理导航栏是否已展开')

        if 'opened' not in client_open_ele:
            self.click_element(home_los.client_management,'点击客户管理')
        self.click_element(home_los.client_list,'点击客户名单')
        time.sleep(1)
        self.input_value(home_los.search_box,account,'搜索框输入主账号')
        self.click_element(home_los.serch_button,'点击搜索按钮')
        time.sleep(1)
        while True:
            if not self.ele_is_visibility(home_los.home_loading):
                break
        self.click_element(home_los.serch_button,'点击搜索按钮')
        time.sleep(1)
        while True:
            if not self.ele_is_visibility(home_los.home_loading):
                break        
        #进入账号详情页
        new_switch_to_account = list(home_los.switch_to_account)
        new_switch_to_account[1] = new_switch_to_account[1].format(account)
        if self.ele_is_visibility(new_switch_to_account):
            self.click_element(new_switch_to_account,f'点击主账号{account}进入账号详情页')

        