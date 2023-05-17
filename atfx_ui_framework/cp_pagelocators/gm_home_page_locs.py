'''
Author: TylerQA 990687322@qq.com
Date: 2023-04-23 17:10:55
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-04-27 11:49:59
FilePath: \atfx_-ui_framework\cp_pagelocators\gm_homepage_locs.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from selenium.webdriver.common.by import By
import sys,os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'tools'))
from global_SystemEnv import SystemEnv

class Gm_Home_Page_Locs(object):

    #页面文本定位，用于断言
    home_text = (By.CSS_SELECTOR,'.nav-title')

    #主账号元素定位
    account_num = (By.CSS_SELECTOR,'.user-name-font')
    #页面验证联系方式弹窗是否出现
    connect_popup = (By.XPATH,"//span[.='Verify Your Contact Information']") if SystemEnv.CP_LANG == 'English' else (By.XPATH,"//span[.='验证您的联系方式']")

    #联系方式确认按钮,-2
    connect_ok_button = (By.XPATH,"//div[@class='el-dialog__wrapper']/div[@aria-label='Verify Your Contact Information']//button[2]") if SystemEnv.CP_LANG == 'English' else (By.XPATH,"//div[@class='el-dialog__wrapper']/div[@aria-label='验证您的联系方式']//button[2]")

    #验证邮箱联系方式
    #图片验证码定位
    img_code_ele = (By.CSS_SELECTOR,"[width='150']")
    #验证码输入框
    code_input = (By.CSS_SELECTOR,".is-required [placeholder='CAPTCHA']") if SystemEnv.CP_LANG == 'English' else (By.CSS_SELECTOR,".is-required [placeholder='验证码']")
    #发送按钮
    send_button = (By.CSS_SELECTOR,'.dialog-sendCode')
    #验证码错误定位
    code_error = (By.CSS_SELECTOR,'.captcha_error')
    #填写邮箱验证码
    email_code_input = (By.XPATH,"//form[@class='el-form']//div[@class='el-row']//input[@class='el-input__inner']")
    #下一步按钮
    next_button = (By.CSS_SELECTOR,'.dialog-submit')
    #跳过手机验证，以后再做
    skip_phone_code = (By.CSS_SELECTOR,'.doItLeTer-css')
    #完成
    submit = (By.CSS_SELECTOR,'.dialog-submit > span')

    #公司申明弹窗
    company_statement = (By.XPATH,"//span[.='公司声明']") if SystemEnv.CP_LANG == '简体中文' else (By.XPATH,"//span[.='Company Declaration']")
    #公司申明条款勾选框
    company_box = (By.CSS_SELECTOR,'.el-checkbox__inner')
    #公司申明弹窗确定按钮
    company_ok = (By.CSS_SELECTOR,'.confirm-btn > span')

    #资料审批弹窗
    under_review = (By.XPATH,"//span[.='资料审批中']") if SystemEnv.CP_LANG == '简体中文' else (By.XPATH,"//span[.='Information Under Review']")
    #确定按钮
    ok_button = (By.CSS_SELECTOR,'.el-button--primary > span')

    #代理申请弹窗
    proxy_ele = (By.XPATH,"//div[@aria-label='代理申请']") if SystemEnv.CP_LANG == '简体中文' else (By.XPATH,"//div[@aria-label='IB Application']")
    #代理申请确认按钮
    proxy_ok = (By.CSS_SELECTOR,'.el-button--primary > span')
    #代理申请返佣表格勾选框
    proxy_box = (By.CSS_SELECTOR,'.ps-agree-bot .el-checkbox__inner')
    #代理申请返佣表格提交按钮
    proxy_submit = (By.CSS_SELECTOR,'.agree-btn')
    
    #审批完成弹窗
    review_success = (By.XPATH,"//span[.='审批成功']") if SystemEnv.CP_LANG == '简体中文' else (By.XPATH,"//span[.='Approved Successfully']")




