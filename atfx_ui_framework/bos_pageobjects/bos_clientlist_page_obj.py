'''
Author: TylerQA 990687322@qq.com
Date: 2023-04-23 21:42:16
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-04-27 11:54:27
FilePath: \atfx_-ui_framework\bos_pageobjects\bos_clientlist_page_obj.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import sys,os,time,re
from loguru import logger
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'tools'))
from global_SystemEnv import SystemEnv
sys.path.append(os.path.join(SystemEnv.BOS_PAGELOCS_DIR))
from basepage import BasePage
from bos_clientlist_page_locs import Bos_ClientList_Page_Locs as client_los
from handle_gen_data import gen_capitalize_str

class Bos_Client_Page_Obj(BasePage):

    #进入客户名单详情页获取邮件验证码
    def get_email_code(self,winindex=0)->str:
        time.sleep(2)
        self.switch_windows(winindex,'切换到客户详情页窗口')
        self.click_element(client_los.email_info,'点击邮件记录')
        time.sleep(1)
        self.click_element(client_los.email_refresh,'刷新邮件记录')
        time.sleep(4)
        self.click_element(client_los.new_email,'点击最新的邮件')
        time.sleep(1)
        email_text = self.get_text(client_los.code_ele,'获取邮件验证码文本')
        logger.info(f'邮件验证码文本：{email_text}')
        email = ''.join(re.findall('\d',email_text))
        return email
    
    #初审
    def review(self,account,winindex=0):
        time.sleep(1)
        self.switch_windows(winindex,'切换到客户详情页窗口')
        time.sleep(1)
        if str(account).startswith('10'):#ib账号初审
            while True:
                if self.ele_is_visibility(client_los.ib_rebate):
                    self.click_element(client_los.ib_rebate,'点击返佣申请表格')
                    break
            time.sleep(2)
            self.click_element(client_los.ibrebate_button,'点击返佣申请开关')
            time.sleep(0.5)
            while True:
                if self.ele_is_visibility(client_los.ibrebate_ok):
                    self.click_element(client_los.ibrebate_ok,'点击确认修改返佣申请')
                    break
            time.sleep(2)
            self.click_element(client_los.account_info,'点击主账户信息')
            time.sleep(1)            
            self.double_click(client_los.ib_link,'双击代理链接')
            time.sleep(0.5)
            self.click_element(client_los.ib_link,'单击选择代理链接')
            time.sleep(0.5)
            #替换定位
            choose_link = list(client_los.choose_link)
            choose_link[1]=choose_link[1].format('A001')
            self.click_element(choose_link,'选择A001代理链接')
            time.sleep(0.5)
            self.double_click(client_los.link_ok,'双击确认代理链接')
            time.sleep(2)
            while True:
                if not self.ele_is_visibility(client_los.loading):
                    break
            time.sleep(2)
            self.double_click(client_los.ib_code,'双击代理代码')
            time.sleep(0.5)
            self.input_value(client_los.ib_code_input,gen_capitalize_str(11),'输入代理代码')
            time.sleep(1)
            self.click_element(client_los.click_ibcode,'确认代理代码')
            time.sleep(2)
            while True:
                if not self.ele_is_visibility(client_los.loading):
                    break
            time.sleep(2)
            self.js_top_or_down('将页面移动至顶部',0)
        #指派
        time.sleep(2)
        while True:
            if self.ele_is_visibility(client_los.assing):
                self.click_element(client_los.assing,'点击指派')
                break
        time.sleep(0.5)  
        self.click_element(client_los.confirm,'指派当前登录用户')
        #指派按钮是否loading
        while True:
            if not self.ele_is_display(client_los.confirm_loading):
                break
        time.sleep(0.5)
        self.click_element(client_los.fitst_process,'点击初审处理中按钮')
        time.sleep(0.5)
        self.click_element(client_los.success_review,'成功初审按钮')
        time.sleep(1)
        self.input_value(client_los.post_code,'845545','输入邮编')
        time.sleep(4)
        self.click_element(client_los.form_submit,'点击表单确认按钮')
        #判断确认按钮是否正则修改状态中
        while True:
            if not self.ele_is_display(client_los.submit_inprocess):
                break
        time.sleep(3)
        self.status = self.get_text(client_los.status,'获取初审完成后的状态')
        self.click_element(client_los.tdaccount,'点击真实账户信息')
        time.sleep(0.5)
        self.tdaccount = self.get_text(client_los.tdaccount_ele,'获取新开交易账号')
        time.sleep(1)
        logger.info(f'审核状态：{self.status}')
        logger.info(f'新开交易账号为：{self.tdaccount}')
        self.close_browser()







