'''
Author: TylerQA 990687322@qq.com
Date: 2023-04-21 01:56:16
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-04-26 18:25:31
FilePath: \atfx_-ui_framework\bos_pageobjects\bos_login_obj.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import sys,os,time
from loguru import logger
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'tools'))
from global_SystemEnv import SystemEnv
sys.path.append(os.path.join(SystemEnv.BOS_PAGELOCS_DIR))
from basepage import BasePage
from bos_login_page_locs import Bos_Login_PageLocs
from bos_home_page_locs import Bos_Home_Page_Locs


class Bos_Login(BasePage):

    #登录bos
    def login_bos(self,username,password,winindex=0):
        self.switch_windows(winindex,'切换到bos窗口')
        #选择登录语言
        self.click_element(Bos_Login_PageLocs.lang_select_box,'点击语言下拉框')
        self.click_element(Bos_Login_PageLocs.lang,'选择语言')
        logger.info(f'选择{SystemEnv.BOS_LANG}语言登录BOS')
        #输入用户名
        self.input_value(Bos_Login_PageLocs.user,username,'输入用户名')
        #输入密码
        self.input_value(Bos_Login_PageLocs.psword,password,'输入密码')
        time.sleep(0.5)
        #点击登录
        self.click_element(Bos_Login_PageLocs.login_button,'登录bos')
        #判断首页代办事项是否出现
        while True:
            if self.ele_is_visibility(Bos_Home_Page_Locs.home_tasks):
                break
        