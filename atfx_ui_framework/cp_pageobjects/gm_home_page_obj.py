'''
Author: TylerQA 990687322@qq.com
Date: 2023-04-23 17:56:03
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-04-27 11:38:23
FilePath: \atfx_-ui_framework\cp_pageobjects\gm_home_page_obj.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import sys,os,time,re
from loguru import logger
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'tools'))
from global_SystemEnv import SystemEnv
sys.path.append(os.path.join(SystemEnv.CP_PAGELOCS_DIR))
from basepage import BasePage
from gm_home_page_locs import Gm_Home_Page_Locs as HomeLocs
from handle_tools import Base64_api


class Gm_Home_Page_Obj(BasePage):


    #获取页面您好/HI文本
    def get_hi_text(self):
        time.sleep(1)
        return self.get_text(HomeLocs.home_text,'获取首页文本')

    #获取主账号文本
    def get_account(self):
        time.sleep(1)
        while True:
            if self.ele_is_visibility(HomeLocs.account_num):
                break
            else:
                continue
        self.account_txt = self.get_text(HomeLocs.account_num,'获取主账号文本')
        accountnum = ''.join(re.findall('\d',self.account_txt))
        logger.info(f'获取登录/注册成功后页面上的主账号:{accountnum}')
        return accountnum

    
    #识别验证码填写验证码
    def discern_email_code(self,country,winindex=0):
        time.sleep(2)
        self.switch_windows(winindex,'切换到CP首页')
        time.sleep(1)
        #判断代理返佣申请表格是否出现
        self.is_proxy_popup()
            
        if country == '中国' or country == 'China':
            logger.info('中国地区账号KYC')
            return False
        else:
            if self.ele_is_display(HomeLocs.connect_popup):#弹窗是否出现
                #截取页面验证码图片
                self.click_element(HomeLocs.connect_ok_button,'点击联系方式弹窗的确认按钮')
                time.sleep(1)
                while True:
                    time.sleep(0.5)
                    img_path = self.elementImage(HomeLocs.img_code_ele,'截取验证码图片')
                    time.sleep(0.5)
                    code = Base64_api(SystemEnv.TUJIAN_USERNAME,SystemEnv.TUJIAN_PSWORD,img_path,SystemEnv.TUJIAN_TYPE)
                    self.input_value(HomeLocs.code_input,code,'填写识别的验证码')
                    time.sleep(0.5)
                    if self.ele_is_visibility(HomeLocs.send_button):
                        self.click_element(HomeLocs.send_button,'点击发送')
                    time.sleep(1)
                    #判断验证码是否正确
                    if self.ele_is_display(HomeLocs.code_error):
                        logger.warning('验证码识别错误，重新识别验证码')
                    else:
                        break
                return True
            else:
                logger.info('该账号邮箱已验证')
                return False           

    #填写邮箱验证码
    def input_email_code(self,code,winindex=0):
        self.switch_windows(winindex,'切换窗口到CP首页')            
        self.input_value(HomeLocs.email_code_input,code,'填写邮箱验证码')
        self.click_element(HomeLocs.next_button,'点击验证邮箱下一步按钮')
        #跳过手机验证
        self.click_element(HomeLocs.skip_phone_code,'跳过手机验证，以后再做')
        time.sleep(0.5)
        self.click_element(HomeLocs.submit,'点击完成')

    #判断公司是否弹出公司申明弹窗
    def company_declaration(self):
        self.driver_refresh()
        time.sleep(2)
        if self.ele_is_display(HomeLocs.company_statement):
            self.click_element(HomeLocs.company_box,'勾选公司申明弹窗协议')
            self.click_element(HomeLocs.company_ok,'点击公司申明确定按钮')

    #判断资料审核中弹窗是否弹出
    def is_under_review(self):
        time.sleep(1)
        if self.ele_is_display(HomeLocs.under_review):
            self.click_element(HomeLocs.ok_button,'点击资料审核中弹窗确认按钮')
            
    #判断代理申请弹窗是否弹出
    def is_proxy_popup(self):
        time.sleep(1)
        if self.ele_is_display(HomeLocs.proxy_ele):
            self.click_element(HomeLocs.proxy_ok,'点击代理申请确认按钮')
            time.sleep(1)
        if self.ele_is_display(HomeLocs.proxy_box):
            self.click_element(HomeLocs.proxy_box,'勾选代理申请返佣表格协议')
            self.click_element(HomeLocs.proxy_submit,'点击代理申请返佣表格确认按钮')

    