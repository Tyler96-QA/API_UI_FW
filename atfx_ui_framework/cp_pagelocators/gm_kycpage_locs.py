from selenium.webdriver.common.by import By
import sys,os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'tools'))
from global_SystemEnv import SystemEnv

class Gm_Kyc_Page_Locs(object):

    #非中国IB/CL用户KYC
    #护照/身份证图片上传定位
    #更改上传元素属性
    upload_change = (By.XPATH,"//p[@class='img-text img-text-required']/../../../../div[2]")#将style属性更改为block。显示上传按钮
    #sendkeys方法上传图片
    upload_ele = (By.CSS_SELECTOR,'.el-upload__input') #直接通过sendkeys上传
    #图片是否上传成功定位
    is_uploaded = (By.CSS_SELECTOR,'.remove-image')
    #出生日期
    brithday = (By.CSS_SELECTOR,"[placeholder='请选择出生日期为DD-MM-YYYY的格式']") if SystemEnv.CP_LANG == '简体中文' else (By.CSS_SELECTOR,"[placeholder='Please select the date of birth with DD-MM-YYYY format']")
    #标签：年
    header_year = (By.CSS_SELECTOR,'.el-date-picker__header > span')
    #年份日期选择框左侧按钮
    year_left = (By.CSS_SELECTOR,'.el-icon-d-arrow-left')
    #具体年份(1-10可选)
    year = (By.CSS_SELECTOR,'.el-year-table tr > td > .cell')
    #具体月份(1-12可选)
    month = (By.CSS_SELECTOR,'.el-month-table tr > td .cell')
    #具体日期(1-30)可选
    day = (By.CSS_SELECTOR,'.el-date-table tr > .available span')
    #性别(1-2随机)
    sex = (By.CSS_SELECTOR,'.el-radio > .el-radio__label')
    #证件号码
    id_code = (By.CSS_SELECTOR,"[placeholder='请输入证件号码']") if SystemEnv.CP_LANG == '简体中文' else (By.CSS_SELECTOR,"[placeholder='Please fill in the ID number']")
    #居住地址
    address = (By.CSS_SELECTOR,"[placeholder='请输入地址']") if SystemEnv.CP_LANG == '简体中文' else (By.CSS_SELECTOR,"[placeholder='Please fill in your address']")
    #勾选协议
    buniess = (By.CSS_SELECTOR,'.agree-checkbox .el-checkbox__inner')
    #提交按钮
    submit = (By.CSS_SELECTOR,'.submit-btn > span')
    #页面loading
    kyc_loading = (By.CSS_SELECTOR,'.el-loading-mask')
    #成功提交KYC后的提示语
    kyc_sucess = (By.XPATH,"//h2[@class='title']")


    #中国区账号KYC其他元素定位
    #判断是否跳转到第二步，银行资料
    bank_info = (By.XPATH,"//span[.='银行资料']") if SystemEnv.CP_LANG == '简体中文' else (By.XPATH,"//span[.='Bank Info']")
    #银行卡号码
    bank_id = (By.XPATH,"//label[@for='bankCardNo']/../div/div/input")
    #银行名称
    bank_name = (By.XPATH,"//label[@for='bank']/../div/div/input")
    #银行分行名称
    branchName = (By.XPATH,"//label[@for='branchName']/../div/div/input")
    #银行分行省份
    branchProvince = (By.XPATH,"//label[@for='branchProvince']/../div/div/input")
    #银行分行城市
    branchCity = (By.XPATH,"//label[@for='branchCity']/../div/div/input")
    # #持卡人姓名
    # beneficiaryName = (By.XPATH,"//label[@for='beneficiaryName']/../div/div/input")
    #判断是否跳转至第三部，上传个人认证
    personal_verification = (By.XPATH,"//span[.='个人认证']") if SystemEnv.CP_LANG == '简体中文' else (By.XPATH,"//span[.='Personal verification']")
    #上传地址/视频认证
    upload_verify = (By.CSS_SELECTOR,'.el-col-16 div > .btns')
    #地址证明修改元素属性
    address_change_attr = (By.XPATH,"//div[@class='el-upload el-upload--text']/..")
    

    

