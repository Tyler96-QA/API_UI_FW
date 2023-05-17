'''
Author: TylerQA 990687322@qq.com
Date: 2023-04-22 20:11:08
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-04-24 18:19:40
FilePath: \atfx_-ui_framework\cp_pagelocators\gm_register_page_locs.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from selenium.webdriver.common.by import By
import sys,os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'tools'))
from global_SystemEnv import SystemEnv

class Gm_Register_Page_Locs(object):


    #使用限制弹窗是否出现判断
    exist_limit = (By.CSS_SELECTOR,'.el-dialog__wrapper')

    #使用限制弹窗
    use_limit = (By.CLASS_NAME,'blk-sure-btn')

    #语言下拉按钮
    lang_box = (By.XPATH,"//i[@class='el-icon-arrow-down el-icon--right']")

    #选择语言,目前只支持简中及英语
    lang = (By.XPATH,"//li[contains(.,'简体中文')]") if SystemEnv.CP_LANG == '简体中文' else  (By.XPATH,"//li[contains(.,'English')]")

    #居住地下拉框
    live_box = (By.CSS_SELECTOR,'.country-label .el-select__caret')

    #选择居住国家,国家可替换：泰国、南韩......
    check_live = (By.XPATH,"//span[.='{}']")

    #默认选择国家
    default_live = [By.CSS_SELECTOR,"[x-placement='bottom-start'] li:nth-of-type(191)"]

    #名字姓氏等多个输入框
    input_box = (By.XPATH,"//div[@class='el-form-item__content']//input[@class='el-input__inner']")

    #邀请码
    ivn_code = (By.CSS_SELECTOR,'.el-textarea__inner')
    
    #邮箱填写格式错误元素定位
    email_erro_exist = (By.XPATH,"//div[@class='el-form-item__content']/..")

    #邮箱重复提示定位
    email_existed = (By.CSS_SELECTOR,'.labels')
     
    #ATFX标准业务条款勾选框
    business = (By.CSS_SELECTOR,'.el-checkbox__inner')

    #下一步注册按钮
    next_step = (By.CSS_SELECTOR,'.b-confirm > span')

    #已有账号，登录按钮
    login = (By.XPATH,"//div[@class='b-return-l']/a")

