import sys,os,time
from loguru import logger
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'tools'))
from global_SystemEnv import SystemEnv
sys.path.append(os.path.join(SystemEnv.CP_PAGELOCS_DIR))
from basepage import BasePage
from gm_login_locs import Gm_Login_Locs as Los
from gm_home_page_locs import Gm_Home_Page_Locs

class Gm_Login_Obj(BasePage):

    def exist_topup(self):
        time.sleep(2)
        logger.info('判断页面弹窗是否出现')
        limit_attr = self.get_attribute(Los.exist_limit,'style','获取style属性')
        if 'none' not in limit_attr:
            self.click_element(Los.use_limit,'点击页面使用限制弹窗')
            logger.info('去除页面用户使用限制弹窗')
            return True
        
    #选择登录cp语言
    def chose_lang(self):
        self.click_element(Los.lang_box,'点击语言下拉框')
        time.sleep(0.5)
        self.click_element(Los.lang,'选择页面语言')
        time.sleep(1)
        logger.info(f'选择{SystemEnv.CP_LANG}语言登录')

    #登录
    def login_cp_gm(self,email,password,winindex=0):
        self.switch_windows(winindex,'切换到CP窗口')
        self.exist_topup()
        self.chose_lang()
        self.input_value(Los.input_box,email,'输入邮箱',2)
        self.input_value(Los.input_box,password,'输入密码',4)
        time.sleep(0.5)
        self.click_element(Los.login_button,'点击登录')
        time.sleep(1)
        #判断首页账号ID是否出现
        while True:
            if self.ele_is_visibility(Gm_Home_Page_Locs.account_num):
                break