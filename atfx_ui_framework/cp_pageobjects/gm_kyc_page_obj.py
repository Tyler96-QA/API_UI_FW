'''
Author: TylerQA 990687322@qq.com
Date: 2023-04-24 11:04:16
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-04-27 11:45:44
FilePath: \atfx_-ui_framework\cp_pageobjects\gm_kyc_page_obj.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

import sys,os,time,random
from loguru import logger
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'tools'))
from global_SystemEnv import SystemEnv
from handle_gen_data import gen_cur_time, gen_random_code,gen_random_address,gen_random_city,gen_random_province
sys.path.append(os.path.join(SystemEnv.CP_PAGELOCS_DIR))
from basepage import BasePage
from gm_kycpage_locs import Gm_Kyc_Page_Locs as kyc_los

class Gm_Kyc_Obj(BasePage):

    def kyc_actions(self,country):
        if country == '中国' or country == 'China':
            logger.info('中国地区KYC操作')
            self.china_kyc()
            time.sleep(2)
        else:
            logger.info('非中国地区用户KYC')
            time.sleep(2)
            #更改上传图片input标签属性
            self.js_change_attr(kyc_los.upload_change,'style',r'display:\block','更改上传图片属性')
            time.sleep(1)
            while True:
                if 'none' in self.get_attribute(kyc_los.is_uploaded,'style','获取上传图片元素的style属性'):
                    self.input_imgs(kyc_los.upload_ele,os.path.join(SystemEnv.IMGS_DIR,'CAT.jpg'),'上传证件照')
                    time.sleep(2)
                else:
                    break
            #选择出生日期
            self.click_element(kyc_los.brithday,'选择出生日期')
            time.sleep(0.5)
            self.click_element(kyc_los.header_year,'选择年份')
            time.sleep(0.5)
            self.click_element(kyc_los.year_left,'点击左侧切换按钮，切换年份')
            self.double_click(kyc_los.year_left,'双击，切换年份')
            time.sleep(1)
            self.click_element(kyc_los.year,'随机选择年份',random.randint(1,10))
            self.click_element(kyc_los.month,'随机选择月份',random.randint(1,12))
            self.click_element(kyc_los.day,'随机选择日期',random.randint(1,30))
            time.sleep(0.5)
            self.element_focus(kyc_los.submit,'元素聚焦')
            self.click_element(kyc_los.sex,'随机选择性别',random.randint(1,2))
            self.input_value(kyc_los.id_code,gen_random_code(),'输入随机证件号码')
            self.input_value(kyc_los.address,gen_random_address(),'输入随机地址')
            self.click_element(kyc_los.buniess,'勾选协议')
        time.sleep(3)
        self.click_element(kyc_los.submit,'点击提交')

        while True:
            if self.ele_is_visibility(kyc_los.kyc_sucess):
                break
        self.success_text = self.get_text(kyc_los.kyc_sucess,'获取Kyc成功后的文本')


    def china_kyc(self):
        #第一步
        logger.info('中国KYC第一步验证:上传身份证')
        time.sleep(2)
        while True:
            if self.ele_is_display(kyc_los.upload_change):
                break
        self.js_change_attr(kyc_los.upload_change,'style',r'display:\block','更改上传身份证正面图片元素属性')
        time.sleep(1)
        self.js_change_attr(kyc_los.upload_change,'style',r'display:\block','更改上传身份证反面图片元素属性',2)
        time.sleep(1)
        while True:
            if 'none' in self.get_attribute(kyc_los.is_uploaded,'style','获取上传图片元素的style属性'):
                self.input_imgs(kyc_los.upload_ele,os.path.join(SystemEnv.IMGS_DIR,'front.jpg'),'上传身份证正面')
                time.sleep(2)
            else:
                break
        while True:
            if 'none' in self.get_attribute(kyc_los.is_uploaded,'style','获取上传图片元素的style属性',2):
                self.input_imgs(kyc_los.upload_ele,os.path.join(SystemEnv.IMGS_DIR,'behind.jpg'),'上传身份证反面',2)
                time.sleep(2)
            else:
                break
        time.sleep(2)
        self.click_element(kyc_los.submit,'点击提交，下一步')
        #第二步
        logger.info('中国KYC第二步验证：上传银行卡')
        while True:
            if self.ele_is_visibility(kyc_los.bank_info):
                break
        #更改银行卡上传style属性
        time.sleep(2)
        self.js_change_attr(kyc_los.upload_change,'style',r'display:\block','更改上传银行卡元素属性')
        time.sleep(1)
        while True:
            if 'none' in self.get_attribute(kyc_los.is_uploaded,'style','获取上传图片元素的style属性'):
                self.input_imgs(kyc_los.upload_ele,os.path.join(SystemEnv.IMGS_DIR,'bear.png'),'上传银行卡')
                time.sleep(2)
            else:
                break
        self.input_value(kyc_los.bank_id,gen_cur_time(),'输入银行卡号码')
        self.input_value(kyc_los.bank_name,'TestBankName','输入银行名称')
        self.input_value(kyc_los.branchName,'branchName','输入分行名称')
        self.input_value(kyc_los.branchProvince,gen_random_province(),'输入分行省份')
        self.input_value(kyc_los.branchCity,gen_random_city(),'输入分行城市')
        self.click_element(kyc_los.buniess,'勾选协议')
        time.sleep(1)
        self.click_element(kyc_los.submit,'点击提交，下一步')
        #第三步
        logger.info('中国kyc第三步，上传地址证明')
        while True:
            if self.ele_is_visibility(kyc_los.personal_verification):
                break
        self.click_element(kyc_los.upload_verify,'点击上传地址认证')
        time.sleep(1)
        self.js_change_attr(kyc_los.address_change_attr,'style',r'display:\block','更改上传地址证明元素属性')
        while True:
            if 'none' in self.get_attribute(kyc_los.is_uploaded,'style','获取上传图片元素的style属性'):
                self.input_imgs(kyc_los.upload_ele,os.path.join(SystemEnv.IMGS_DIR,'bear.png'),'上传地址证明')
                time.sleep(2)
            else:
                break