'''
Author: TylerQA 990687322@qq.com
Date: 2023-04-22 21:03:49
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-04-26 18:41:21
FilePath: \atfx_-ui_framework\cp_pageobjects\gm_register_obj.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import sys,os,time
from loguru import logger
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'tools'))
from global_SystemEnv import SystemEnv
from handle_excel import HandleExcel
from handle_gen_data import gen_cur_time
sys.path.append(os.path.join(SystemEnv.CP_PAGELOCS_DIR))
from basepage import BasePage
from gm_register_page_locs import Gm_Register_Page_Locs as Los
from gm_home_page_locs import Gm_Home_Page_Locs as HomeLocs

handle_data = HandleExcel(os.path.join(SystemEnv.DATA_DIR,'testcases.xlsx'),'gm_register')
kyc_data = HandleExcel(os.path.join(SystemEnv.DATA_DIR,'testcases.xlsx'),'gm_kyc')

class Gm_Register_Page_Obj(BasePage):

    #判断弹窗是否出现，出现则点击
    def is_limit_exist(self):
        time.sleep(2)
        logger.info('判断页面弹窗是否出现')
        if 'none' not in self.get_attribute(Los.exist_limit,'style','获取style属性'):
            self.click_element(Los.use_limit,'点击页面使用限制弹窗')
            logger.info('去除页面用户使用限制弹窗')
            return True
        
    #选择登录cp语言
    def chose_lang(self):
        self.click_element(Los.lang_box,'点击语言下拉框')
        time.sleep(0.5)
        self.click_element(Los.lang,'选择页面语言')
        time.sleep(1)
        logger.info(f'选择{SystemEnv.CP_LANG}语言注册')
    
    #填写注册表单
    def fill_register_form(self,livecountry,name,sruname,phone,email,password,index,inv_code=None):
        if livecountry == '中国' or livecountry == 'China':
            if inv_code == None:
                logger.warning('地区为中国时。邀请码必填')
                raise KeyError('居住国家为中国时邀请码不能为空')
        
        self.click_element(Los.live_box,'点击居住国家下拉框')
        time.sleep(0.5)
        #元素定位替换
        new_check_live = list(Los.check_live)
        new_check_live[1]=new_check_live[1].format(livecountry)
        self.click_element(new_check_live,'选择居住国家')
        time.sleep(0.5)
        #判断国家限制弹窗是否出现
        if self.is_limit_exist():
            self.save_pageshots(f'居住国家被限制，{livecountry}国家注册')
            logger.warning('您选择的国家被限制注册，默认选择泰国')
            self.click_element(Los.live_box,'重新点击居住国家下拉框')
            time.sleep(0.5)
            self.click_element(Los.default_live,'默认选择泰国')
            #更新用例数据，居住国家为南韩
            handle_data.sava_excel_data('C',index,'泰国')
            kyc_data.sava_excel_data('E',index,'泰国') 
        kyc_data.sava_excel_data('E',index,livecountry)    

        
        self.input_value(Los.input_box,name,'输入姓名',2)
        self.input_value(Los.input_box,sruname,'输入姓氏',3)
        self.input_value(Los.input_box,phone,'输入手机号',5)
        self.input_value(Los.input_box,email,'输入邮箱',6)
        self.input_value(Los.input_box,password,'输入密码',7)
        time.sleep(1)
        if 'is-error' in self.get_attribute(Los.email_erro_exist,'class','获取判断邮箱输入是否正确的class属性',6) or self.ele_is_display(Los.email_existed):
            self.save_pageshots(f'邮箱格式错误或已注册，填写{email}邮箱注册')
            email = gen_cur_time()+'@qq.com'
            logger.warning(f'邮箱格式错误或已注册，重新输入随机邮箱:{email}')
            self.input_value(Los.input_box,email,'重新输入随机邮箱',6)
        handle_data.sava_excel_data(7,index,email)
        kyc_data.sava_excel_data(3,index,email)
        logger.info(f'数据共享，将更新后的邮箱作为下一个流程的测试数据：{email}')
        setattr(SystemEnv,f'email{index}',email)

        
        self.input_value(Los.input_box,'GVLS','输入验证码',8)
        if inv_code:
            self.input_value(Los.ivn_code,inv_code,'输入邀请码')
        self.click_element(Los.business,'勾选条款')
        time.sleep(1)
        self.click_element(Los.next_step,'提交注册表单')
        #判断是否进入首页
        while True:
            if self.ele_is_visibility(HomeLocs.account_num):
                break
