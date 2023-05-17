'''
Author: TylerQA 990687322@qq.com
Date: 2023-04-23 21:20:57
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-04-26 16:50:09
FilePath: \atfx_-ui_framework\bos_pagelocators\bos_clientlist_page_locs.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from selenium.webdriver.common.by import By
import sys,os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'tools'))
from global_SystemEnv import SystemEnv

class Bos_ClientList_Page_Locs(object):
    
    #客户名单详情页元素定位
    #右边导航栏定位
    #真实账号信息
    tdaccount = (By.CSS_SELECTOR,"[href='#tdAccount']")

    #主账户信息
    account_info = (By.CSS_SELECTOR,"[href='#masterAccount']")

    #邮件记录
    email_info = (By.CSS_SELECTOR,"[href='#emailRecored']")

    
    #邮件记录刷新按钮
    email_refresh = (By.XPATH,"//div[@class='emailRecord-page']//span[contains(.,'刷新')]") if SystemEnv.BOS_LANG =='简体中文' else (By.XPATH,"//div[@class='emailRecord-page']//span[contains(.,'Refresh')]")

    #最新邮件
    new_email = (By.XPATH,"//div[@class='emailRecod-table ivu-table-wrapper ivu-table-wrapper-with-border']/div/div[2]/table/tbody/tr[1]/td[3]//a")

    #邮箱验证码元素定位
    code_ele = (By.CSS_SELECTOR,"[bgcolor='#ffffff'][width='598'] span")

    #指派按钮
    assing = (By.XPATH,"//span[.='指派']") if SystemEnv.BOS_LANG =='简体中文' else (By.XPATH,"//span[.='Assign']")

    #指派人列表确认按钮
    confirm = (By.XPATH,"//div[@class='ivu-modal-wrap']//span[.='确定']") if SystemEnv.BOS_LANG =='简体中文' else (By.XPATH,"//div[@class='ivu-modal-wrap']//span[.='Confirm']")

    #确认按钮是否loading，是否出现
    confirm_loading = (By.XPATH,"//div[@class='ivu-modal-wrap']//span[.='确定']/../i")
    
    #初审修改状态处理中
    process = (By.XPATH,"//button[@class='ivu-btn ivu-btn-default']/span/span[2]")

    #初审处理中按钮
    fitst_process = (By.XPATH,"//button[@class='ivu-btn ivu-btn-default']/span/span[contains(.,'初审处理中')]") if SystemEnv.BOS_LANG =='简体中文' else (By.XPATH,"//button[@class='ivu-btn ivu-btn-default']/span/span[contains(.,'1st Review In Progress')]")

    #初审完成按钮
    success_review = (By.XPATH,"//li[contains(.,'成功(初审)')]") if SystemEnv.BOS_LANG =='简体中文' else (By.XPATH,"//li[contains(.,'Successful (1st Review)')]")

    #表单邮编输入框
    post_code = (By.XPATH,"//label[.='邮编']/../div/div/input") if SystemEnv.BOS_LANG =='简体中文' else (By.XPATH,"//label[.='Postcode']/../div/div/input")

    #表单确认按钮
    form_submit = (By.XPATH,"//div[@class='ivu-modal-wrap']//span[1]/span[contains(.,'确定')]") if SystemEnv.BOS_LANG =='简体中文' else (By.XPATH,"//div[@class='ivu-modal-wrap']//span[1]/span[contains(.,'Confirm')]")

    #确认按钮正在修改状态中
    submit_inprocess = (By.XPATH,"//div[@class='ivu-modal-wrap']//span[1]/span[2]")
    #状态修改完成后的状态
    status = (By.XPATH,"//div[@class='ivu-dropdown']/div/button/span/span")
    
    #交易账号定位
    tdaccount_ele = (By.XPATH,"//span[.='交易账号']/../../../../../../../div[2]//tbody/tr[1]/td[1]//span[1]")

    #返佣申请表格
    ib_rebate = (By.CSS_SELECTOR,"[href='#ibRebate']")
    #返佣申请表格点击按钮
    ibrebate_button = (By.XPATH,"//span[.='审核: ']/../span[2]") if SystemEnv.BOS_LANG =='简体中文' else (By.XPATH,"//span[.='Verify: ']/../span[2]")
    #确认按钮
    ibrebate_ok = (By.CSS_SELECTOR,'.ivu-modal-confirm-footer > .ivu-btn-primary > span')
    #代理代码
    ib_code = (By.XPATH,"//label[.='代理代码']/../div/div") if SystemEnv.BOS_LANG =='简体中文' else (By.XPATH,"//label[.='IB code']/../div/div")
    #输入代理代码
    ib_code_input = (By.XPATH,"//label[.='代理代码']/../div/div//input") if SystemEnv.BOS_LANG =='简体中文' else (By.XPATH,"//label[.='IB code']/../div/div//input")
    #确认代理代码
    click_ibcode = (By.XPATH,"//label[.='代理代码']/../div/button[2]") if SystemEnv.BOS_LANG =='简体中文' else (By.XPATH,"//label[.='IB code']/../div/button[2]")
    #代理链接按钮
    ib_link = (By.XPATH,"//label[.='代理链接']/../div/div") if SystemEnv.BOS_LANG =='简体中文' else (By.XPATH,"//label[.='IB link']/../div/div")
    #选择代理链接,可替换定位
    choose_link = (By.XPATH,"//li[.='{}']")
    #确认按钮
    link_ok = (By.CSS_SELECTOR,'.ivu-icon-md-checkmark')
    #判断loading,获取style属性
    loading = (By.CSS_SELECTOR,'.spin-icon-load')




