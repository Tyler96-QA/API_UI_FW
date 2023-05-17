'''
Author: TylerQA 990687322@qq.com
Date: 2023-04-21 01:42:16
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-04-22 20:00:06
FilePath: \atfx_-ui_framework\pagelocators\bos_login_page_locs.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from selenium.webdriver.common.by import By
import sys,os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'tools'))
from global_SystemEnv import SystemEnv

class Bos_Login_PageLocs(object):

    #选择语言下拉框
    lang_select_box = (By.CSS_SELECTOR,'.ivu-icon-ios-arrow-down')

    #语言选择
    lang = (By.XPATH,"//li[.='简体中文']") if SystemEnv.BOS_LANG =='简体中文' else (By.XPATH,"//li[.='English']")

    #用户名定位元素
    user = (By.CSS_SELECTOR,"[placeholder='账号']") if SystemEnv.BOS_LANG =='简体中文' else (By.CSS_SELECTOR,"[placeholder='Account']")

    #密码定位元素
    psword = (By.CSS_SELECTOR,"[placeholder='密码']") if SystemEnv.BOS_LANG =='简体中文' else (By.CSS_SELECTOR,"[placeholder='Password']")

    #登录按钮元素定位
    login_button = (By.CSS_SELECTOR,".ivu-btn-large > span")

    #登录loading
    login_loading = (By.CSS_SELECTOR,'.ivu-spin-dot')
