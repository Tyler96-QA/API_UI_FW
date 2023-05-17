'''
Author: Tyler96-QA 1718459369@qq.com
Date: 2023-04-14 02:17:09
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-05-10 21:57:50
FilePath: \Api_test\api_framework_v1\tools\handle_requests.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
"""
封装基于项目特色的请求
"""
import requests
import json as js
from urllib.parse import urlparse
from global_SystemEnv import SystemEnv
from loguru import logger
import allure,os
from handle_aes import encryptData
from handle_assert import assert_db, assert_resp
from handle_extract import handleExtract
from handle_image_captcha import verify_img_code
from handle_pre_sql import exeure_sql_set_gobalattr
from handle_replace_mark import replace_mark_by_data
from handle_reponse import change_resp_to_dict


class HandelRequests(object):

    session = requests.session() #在一个session回话下访问所有接口

    @classmethod
    def request(cls,method:str,url:str,json:str=None,data:str=None,files:str=None,params:str=None,token:str=None):
        
        if json:
            try:
                json = js.loads(json) #json字符串转字典
                logger.info(f'通过json.loads方法将json字符串转换为字典作为请求数据，json请求数据为dict：\n{json}')
            except:
                try:
                    json = eval(json)
                    logger.warning(f'通过json.loads方法将json字符串转换字典失败，请规范请求数据的json格式！返回eval转换的dict：{json}')
                except:
                    logger.error('请检查json请求参数是否符合规范！！！')
                    raise AttributeError('请检查请求参数是否符合规范')

        if files:
            try:
                files = eval(files) #python字符串转字典
                logger.info(f'通过eval方法将python字符串转换为字典作为请求数据，files请求数据为dict：files参数：\n{files}')
            except:
                try:
                    files = js.loads(files)
                    logger.warning(f'通过eval方法将python字符串转换字典失败，请规范请求数据的python字符串格式！返回json.loads转换的dict：files参数：\n{files}')
                except:
                    logger.error('请检查files请求参数是否符合规范！！！')
                    raise AttributeError('请检查请求参数是否符合规范')

        if params:
            try:
                params = eval(params)
                logger.info(f'将python字符串转换为字典作为请求数据，params请求数据为dict：\n{params}')
            except:
                params  = params
                logger.error(f'python字符串转换字典失败，返回字符串：\n{params}')
                raise AttributeError('请检查请求参数是否符合规范')
        
        if data:
            try:
                data = eval(data)
                logger.info(f'将python字符串转换为字典作为请求数据，data请求数据为dict：\n{data}')
            except:
                data  = data
                logger.error(f'python字符串转换字典失败，返回字符串：\n{data}')
                raise AttributeError('请检查请求参数是否符合规范')
 
        cls.header = {}  #新增一个类属性
        if urlparse(url).hostname == urlparse(SystemEnv.BOS_API.get(SystemEnv.ENVIRONMENT)).hostname: #BOS接口
            if token:
                cls.header['accept-language'] = 'zh,zh-CN;q=0.9,en;q=0.8'
                cls.header['authentication'] = token
                logger.info(f'该请求需要token鉴权，发送请求的headers为：{cls.header}')
        else:#CPgm2.0/mu2.0接口
            if token:
                cls.header = {
                    "Origin": SystemEnv.CP_URL.get(SystemEnv.ENTITY).get(SystemEnv.ENVIRONMENT),
                    'x-token':token}
                logger.info(f'该请求需要token鉴权，发送请求的headers为：{cls.header}')
        with allure.step(f'发起请求，请求url：{url}，\n请求头：{cls.header},\n请求数据：json:{json};\ndata:{data};\nfiles:{files};\nparams:{params}'):
            logger.info(f'通过{method}方法发送请求，url：{url}')
        return cls.session.request(method=method,url=url,json=json,data=data,files=files,params=params,headers=cls.header)


def public_request(case:object):
    #=======================================================================================接口测试流程====================================================================

    #=======================================================================================发起请求之前==================================================================：
    
    #1.请求数据中是否有要替换的mark（#**#），如果有则用环境变量（配置文件、数据库读取、接口返回）或者python方法返回值进行替换：
    logger.info(f'开始用例：//////////////////////////////////////////////////////{case.title}//////////////////////////////////////////////////')
    case.url = replace_mark_by_data(case.url)
    with allure.step('请求发送以前，对请求数据进行内置方法处理：'):
        #1.1 有前置sql要执行前置sql，前置sql中有要替换的mark要进行替换
        if case.sql:
            logger.info('处理前置sql，判断前置sql中有要替换的mark')
            exeure_sql_set_gobalattr(case.sql)
        
        #1.2 请求数据中有要替换的mark要进行替换
        if case.req_json:
            with allure.step('请求数据json是否有要替换的占位符'):
                logger.info('请求数据json是否有要替换的占位符')
                print(case.req_json)
                case.req_json_new = replace_mark_by_data(case.req_json)

            #1.2.1 请求数据是否需要加密
            if case.encrypt_key:
                with allure.step('请求数据需要加密，通过AES加密传参'):
                    logger.info('请求数据需要加密，通过AES加密传参')
                    encryp_data = encryptData(SystemEnv.VUE_APP_API_ENCRYPT_KEY,
                                              SystemEnv.VUE_APP_API_ENCRYPT_IV,
                                              case.req_json_new.replace('None','null').replace('True','true').replace('False','false'))
                    case.req_json_new = str({case.encrypt_key:encryp_data})
                    logger.info(f'最终传入的加密参数为：{case.req_json_new}')
        else:
            case.req_json_new = case.req_json
        
        if case.req_params:
            with allure.step('请求数据params是否有要替换的占位符'):
                logger.info('判断求数据params是否有需要替换的mark')
                case.req_params_new = replace_mark_by_data(case.req_params)
        else:
            case.req_params_new = case.req_params

        if case.req_data:
            with allure.step('请求数据data是否有要替换的占位符'):
                logger.info('请求数据data是否有要替换的占位符')
                case.req_data_new = replace_mark_by_data(case.req_data)
        else:
            case.req_data_new = case.req_data

        if case.req_files:
            with allure.step('判断请求数据files中是否有需要替换的占位符'):
                logger.info('判断请求数据files中是否有需要替换的占位符')
                case.req_files_new = replace_mark_by_data(case.req_files)
        else:
            case.req_files_new = case.req_files

        
        #1.3 判断是BOS还是CP的接口，是否要携带各自的token发起请求
        if urlparse(case.url).hostname == urlparse(SystemEnv.BOS_API.get(SystemEnv.ENVIRONMENT)).hostname: #BOS接口
            if hasattr(SystemEnv,'bos_token') and case.url != SystemEnv.BOS_API.get(SystemEnv.ENVIRONMENT):#BOS的其他非登录接口
                with allure.step(f'该请求需要传递token，从系统变量中获取bos_token：{SystemEnv.bos_token},请求域名：{urlparse(case.url).hostname}'):
                    token = SystemEnv.bos_token
                logger.info(f'该请求需要传递token，从系统变量中获取bos_token：{SystemEnv.bos_token},\t请求域名：{urlparse(case.url).hostname}')
            else:
                with allure.step(f'该请求不需要传递token，请求域名：{urlparse(case.url).hostname}'):
                    token = None
                logger.info(f'该请求不需要传递token，请求域名：{urlparse(case.url).hostname}')
        else:#CP-gm/mu2.0接口
            if hasattr(SystemEnv,'cp_token') and 'login' not in case.url.lower():#且不是登录接口
                with allure.step(f'该请求需要传递token，从系统变量中获取cp_token：{SystemEnv.cp_token},\t请求域名：{urlparse(case.url).hostname}'):
                    token = SystemEnv.cp_token
                logger.info(f'该请求需要传递token，从系统变量中获取cp_token：{SystemEnv.cp_token},请求域名：{urlparse(case.url).hostname}')
            else:
                with allure.step(f'该请求不需要传递token，请求域名：{urlparse(case.url).hostname}'):
                    token = None
                logger.info(f'该请求不需要传递token，请求域名：{urlparse(case.url).hostname}')
    
    #=======================================================================================发起请求==================================================================
    with allure.step('发起http/https请求'):
        logger.info('发起请求')
        resp = HandelRequests.request(case.method,
                                        case.url.strip(),
                                        files=case.req_files_new,
                                        data=case.req_data_new,
                                        json=case.req_json_new,
                                        params=case.req_params_new,
                                        token=token)
    
    #======================================================================================发起请求之后==================================================================

    #2判断响应内容是否可以转成字典,不能则转换成字典，key值为extract列的key（如果extract列有值，没有可以自定义key
    with allure.step('处理响应数据'):
        resp_dict = change_resp_to_dict(case.resp_decrypt,resp)
    
        #3.当接口返回图片时
        if case.captcha_code:
            with allure.step('接口返回的是一个二进制图片'):
                logger.info('需要识别二进制图片验证码并将验证码设置为全局变量')
                verify_img_code(resp)
    
        #3.1判断是否要从响应数据中提取数据作为全局变量
        if case.extract:
            with allure.step('从响应结果中提取数据设置为全局变量'):
                logger.info('需要从响应内容中提取数据作为全局变量')
                handleExtract(case.extract,resp_dict)
        else:
            logger.info('不需要从响应内容中提取数据作为全局变量')
        
        #4.是否需要断言
        #4.1有预期结果才去断言
        if case.excepted_actions:
            with allure.step('断言响应数据'):   
                logger.info('断言响应数据是否与预期一致:')
                #断言
                assert_resp(resp_dict,case.excepted_actions)

        #4.2需要数据库断言
        if case.excepted_db:
            with allure.step('断言数据库'):
                logger.info('数据库断言：')
                assert_db(case.excepted_db)