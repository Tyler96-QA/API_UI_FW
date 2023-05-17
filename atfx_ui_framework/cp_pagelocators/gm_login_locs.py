from selenium.webdriver.common.by import By
import sys,os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'tools'))
from global_SystemEnv import SystemEnv

class Gm_Login_Locs(object):

    #使用限制弹窗是否出现判断
    exist_limit = (By.CSS_SELECTOR,'.el-dialog__wrapper')

    #使用限制弹窗
    use_limit = (By.CLASS_NAME,'blk-sure-btn')

    #语言下拉按钮
    lang_box = (By.XPATH,"//i[@class='el-icon-arrow-down el-icon--right']")

    #选择语言,目前只支持简中及英语
    lang = (By.XPATH,"//li[contains(.,'简体中文')]") if SystemEnv.CP_LANG == '简体中文' else  (By.XPATH,"//li[contains(.,'English')]")

    #表单输入框，电子邮件：2，密码：4
    input_box = (By.CSS_SELECTOR,".el-input__inner")

    #登录按钮
    login_button = (By.CSS_SELECTOR,'.login-btn > span')

    #判断登录是否loading
    login_loading = (By.CSS_SELECTOR,'.el-loading-mask')