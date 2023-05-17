'''
Author: TylerQA 990687322@qq.com
Date: 2023-04-21 00:43:33
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-05-10 20:17:29
FilePath: \atfx_api\testcase\conftest.py
Description: 前置与后置，自定义hooks方法
'''
import requests,os,sys
import json as js
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'tools'))
from global_SystemEnv import SystemEnv
from handle_requests import HandelRequests
from handle_image_captcha import verify_img_code
from handle_extract import handleExtract
from handle_database import DatabaseOperate
import pytest
from loguru import logger
from jsonpath import jsonpath


env = SystemEnv.ENVIRONMENT
data_base = DatabaseOperate()
#======================================================================用例的预置条件与环境恢复======================================================================================
@pytest.fixture(scope='class')
def bos_login():
    #从环境变量中获取bos登录信息，区分sit/uat
    login_url = SystemEnv.BOS_API.get(env)
    method = 'post'
    username = SystemEnv.BOS_USERINFO.get(env).get('username')
    password = data_base.search_in_mongodb(SystemEnv.MONGODB.get('uri'),
                                           'atfx-{}'.format(env),
                                           'bos_auth_users',
                                           {'account':username},
                                           'passwd')[0].get('passwd')

    req_dict = {"account": f"{username}", "passwd": f"{password}"}
    logger.info(f'前置：bos {env}环境登录信息：用户名：{username}；密码：{password}')
    try:
        resp = requests.request(method,login_url,json=req_dict)
    except:
        logger.error(f'前置登录bos{env}环境失败')
        raise 
    else:
        token = jsonpath(resp.json(),"$..token")[0]
    setattr(SystemEnv,'bos_token',token)
    logger.info(f'设置全局变量bos_token为：{token}')
    yield

#获取IP地址
@pytest.fixture(scope='session')
def get_ipinfo():
    ip_url = 'https://ipapi.co/json' 
    resp = HandelRequests.request('get',ip_url)
    ip = resp.json().get('ip')
    setattr(SystemEnv,'ip',ip)
    yield 


#出入金接口前置
@pytest.fixture(scope='class',autouse=True) #优先执行
def deposit_withdrawal_info():
    #设置全局变量account与tdaccount
    account,tdaccount = SystemEnv.TEST_INFO.get(SystemEnv.ENTITY).get(env)
    bos_user = SystemEnv.BOS_USERINFO.get(env).get('username')
    domain = SystemEnv.CP_URL.get(SystemEnv.ENTITY).get(env)
    setattr(SystemEnv,'account',account)
    setattr(SystemEnv,'tdaccount',tdaccount)
    setattr(SystemEnv,'bos_user',bos_user)
    setattr(SystemEnv,'bos_user2','tyler.tang2')
    setattr(SystemEnv,'domain',domain)
    yield


#出金接口前置
@pytest.fixture(scope='class')
def from_bos_to_cp_get_token(deposit_withdrawal_info): #此fixture依赖于deposit_withdrawal_inf夹具
    bos_login_url = SystemEnv.BOS_API.get(env)
    bos_to_cp_url = SystemEnv.BOS_TO_CP_API.get(env)
    bos_auth_users = data_base.search_in_mongodb(SystemEnv.MONGODB.get('uri'),
                                         f'atfx-{env}',
                                         'bos_auth_users',
                                         {'account':f'{SystemEnv.bos_user}'},
                                         'passwd',
                                         N=1)
    passwd = bos_auth_users[0].get('passwd')
    login_json = {"account":SystemEnv.bos_user,
                  "passwd":passwd}
    bos_login_resp = HandelRequests.request('post',bos_login_url,json=js.dumps(login_json))
    setattr(SystemEnv,'bos_token',jsonpath(bos_login_resp.json(),"$..token")[0])

    bos_to_cp_json = {"domain":SystemEnv.domain,
                      "loginType":"accountNumber",
                      "loginNumber":SystemEnv.account,
                      "lang":"hk",
                      "entity":SystemEnv.AREA,
                      "ip":"202.85.14.161"}
    bos_to_cp_resp = HandelRequests.request('post',bos_to_cp_url,json=js.dumps(bos_to_cp_json),token=SystemEnv.bos_token)

    setattr(SystemEnv,'cp_token',jsonpath(bos_to_cp_resp.json(),"$..id_token")[0])
    yield
    delattr(SystemEnv,'bos_token')
    delattr(SystemEnv,'cp_token')



@pytest.fixture()
def verify_code():
    logger.info('============运行用例前置：verify_code，满足用例的预置条件==============')
    captcha_url = SystemEnv.CAPTCHA.get(SystemEnv.ENTITY).get(env)
    if hasattr(SystemEnv,'cp_token'):
        token = getattr(SystemEnv,'cp_token')
    else:
        token = None
    captcha_resp = HandelRequests.request('get',captcha_url,token=token)
    #设置全局变量
    verify_img_code(captcha_resp)
    handleExtract('{"captchaid":"$..id"}',captcha_resp.json())
    yield
    #环境恢复，删除全局变量
    logger.info('运行用例后置：verify_code，环境恢复：删除设置的全局变量')
    delattr(SystemEnv,'imgcode')
    delattr(SystemEnv,'captchaid')

#==============================================================================配置全局hooks方法=========================================================================================
# 用例收集以后
# 当用例title包含"验证码"时，需要运行前置夹具verify_code：发送验证码并识别验证码
def pytest_collection_modifyitems(items):
    logger.info('================================================开始为每个用例加上必须夹具=======================================================')
    itmes_list_change = []
    items_list_unchange = []
    for item in items:
        case_title = item.callspec.params.get('case').title
        if '验证码' in case_title:
            itmes_list_change.append(item)
        else:
            items_list_unchange.append(item)
    for nochange in items_list_unchange:
        nochange.fixturenames = tuple(nochange.fixturenames)
    for change in itmes_list_change:
        logger.info('需要加上前置方法 verify_code 的用例为：{};title: {}'.format(change.nodeid,change.callspec.params.get('case').title))
        change.fixturenames.append('verify_code')
    for nochange in items_list_unchange:
        nochange.fixturenames = list(nochange.fixturenames)



#用例执前输出每个阶段的执行报告
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # 获取钩子方法的调用结果
    out = yield
    res = out.get_result()
    logger.info(f'====================================================={res.when} 执行结果========================================', out)
    logger.info(f'测试报告:{res}')
    logger.info(f'步骤：{res.when}')
    logger.info(f'nodeid:{res.nodeid}')
    logger.info(f"运行结果：{res.outcome}")
    logger.info(f'耗时：{res.duration}s')
    logger.info(f'====================================================={res.when} 执行结束========================================\n')

