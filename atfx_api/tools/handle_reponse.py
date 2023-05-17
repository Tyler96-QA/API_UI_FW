'''
Author: Tyler96-QA 1718459369@qq.com
Date: 2023-04-13 17:06:19
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-05-10 13:36:46
FilePath: \Api_test\api_framework_v1\tools\handle_reponse.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from loguru import logger
import allure
import json as js
from handle_aes import decryptData
from global_SystemEnv import SystemEnv

@allure.step('将响应数据转换为字典类型')
def change_resp_to_dict(resp_decrypt:str,resp)->dict:
    logger.info(f'响应状态码:{resp.status_code}')

    try:
        with allure.step('将响应的json格式数据转换位字典'):
            resp_dict = resp.json()
    except:
        logger.warning('响应数据不是json格式，无法转换成字典，自动添加key为result转成字典')
        with allure.step('响应数据不是json格式，无法转换成字典，自动添加key为result转成字典'):
            resp_dict = {'result':resp.text}
    #响应数据是否需要解密
    if resp_decrypt:
        with allure.step('响应数据需要解密'):
            logger.info('响应数据需要解密')
            decrypt_str = decryptData(SystemEnv.VUE_APP_API_ENCRYPT_KEY,SystemEnv.VUE_APP_API_ENCRYPT_IV,resp_dict['data'])
            resp_dict['data'] = js.loads(decrypt_str)
    
    with allure.step(f'最终响应结果为：\n{resp_dict}'):
        logger.info(f'最终响应结果为：\n{resp_dict}')
    return resp_dict