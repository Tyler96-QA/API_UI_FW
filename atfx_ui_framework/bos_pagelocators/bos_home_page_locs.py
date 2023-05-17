from selenium.webdriver.common.by import By
import sys,os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'tools'))
from global_SystemEnv import SystemEnv


class Bos_Home_Page_Locs(object):

    #首页代办事项定位
    home_tasks = (By.XPATH,"//strong[.='待办事项，']") if SystemEnv.BOS_LANG =='简体中文' else (By.XPATH,"//strong[.='Pending Tasks,']")

    ##左边导航栏一级标签定位
    #客户管理一级导航是否展开.获取class属性
    client_management_open = (By.CSS_SELECTOR,".ivu-menu-submenu")
    #客户管理
    client_management = (By.XPATH,"//span[.='客户管理']") if SystemEnv.BOS_LANG =='简体中文' else (By.XPATH,"//span[.='Client Management']")
    #资金管理
    fund_management = (By.XPATH,"//span[.='资金管理']") if SystemEnv.BOS_LANG =='简体中文' else (By.XPATH,"//span[.='Fund Management']")
    #公告管理
    announcement_Management = (By.XPATH,"//span[.='公告管理']") if SystemEnv.BOS_LANG =='简体中文' else (By.XPATH,"//span[.='Announcement Management']")

    #二级导航栏定位
    #客户名单
    client_list = (By.XPATH,"//span[.='客户名单']") if SystemEnv.BOS_LANG =='简体中文' else (By.XPATH,"//span[.='Client List']")

    #客户名单GM按钮
    gm_menue = (By.CSS_SELECTOR,'.ivu-btn-group > .ivu-btn-primary')

    #客户名单页面筛选按钮
    client_list_filter = (By.CSS_SELECTOR,'.ivu-input-group-with-append > .ivu-input-group-prepend .ivu-icon')

    #客户名单页筛选下拉框
    #筛选条件：交易账号、主账号、邮箱等
    filter_box = (By.XPATH,"//li[contains(.,' 交易账号 ')]") if SystemEnv.BOS_LANG =='简体中文' else (By.XPATH,"//li[contains(.,'Trading Account')]")
    ...

    #客户名单页搜索框
    search_box = (By.CSS_SELECTOR,'.ivu-input-group-with-append > [placeholder]')

    #客户名单搜索按钮
    serch_button = (By.CSS_SELECTOR,'.ivu-btn-icon-only > .ivu-icon')

    #进入详情页,根据主账号更改定位
    switch_to_account = (By.XPATH,"//a[.='{}']")

    #loading
    home_loading = (By.CSS_SELECTOR,'.ivu-spin-main')