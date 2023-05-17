'''
Author: Tyler96-QA 1718459369@qq.com
Date: 2023-04-15 01:56:10
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-05-12 11:26:42
FilePath: \Api_test\api_framework_v1\tools\handle_assert.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
"""
响应结果断言、数据库断言封装
"""
from handle_replace_mark import replace_mark_by_data
from global_SystemEnv import SystemEnv
from handle_database import DatabaseOperate
import pytest_check as check
import pytest
from loguru import logger
import jsonpath
import allure
import datetime


database = DatabaseOperate()

#响应结果断言
#将从excel中读取的excepted_actions列字符进行占位符替换
#字符串转换为字典，字典的每个key都是要断言的字段
#响应数据中也存在字典中的key
@allure.step('判断断言字符串中是否有要替换的占位符')
def assert_resp(resp_dict:dict,excepted_actions:str)->None:
    logger.info('判断断言字符串中是否有要替换的占位符')
    except_str = replace_mark_by_data(excepted_actions)
    for key,value in eval(except_str).items():
        resp_ = jsonpath.jsonpath(resp_dict,'$..{}'.format(key))[0]
        logger.info(f'断言响应结果中的 {key} 字段的值 {resp_} 是否与预期 {value} 一致')
    try:
        with allure.step(f'断言响应结果中的 {key}字段的值 {resp_} 是否与预期 {value} 一致'):
            pytest.assume(resp_ == value)
            logger.info('断言成功')
    except:
        logger.error('断言失败')
        raise AssertionError(f'断言失败：{resp_} 与 {value} 不一致')


#数据库断言：
#将从excel中读取的数据库断言字符串进行占位符替换（来自于全局变量）
#将字符串转换成列表，列表的成员为字典，每个字典都有sql和check2个key
#sql语句中查询的字段名要与check字典中的key名一致，因为check就是预期的数据库查询结果
#样板：[{"sql":"SELECT STATUS FROM tz_order WHERE order_number = '#orderNumbers#'","check":{"status":2}},{"sql":"SELECT stocks FROM tz_sku WHERE prod_id = '#prodId#'","check":{"stocks":#stocks#-1}}]
@allure.step('对数据库进行断言')
def assert_db(assert_db_str:str)->None:
    logger.info('数据库断言字符串中是否有要替换的占位符')
    assert_replace_str= replace_mark_by_data(assert_db_str)
    for ass in eval(assert_replace_str):
        res = database.search_in_mysql(ass.get('sql'),many=1) #返回一条数据，字典
        exp =ass.get('check')
        dif = res.keys() & exp
        diff_vals = [(k, res[k], exp[k]) for k in dif if res[k] != exp[k]]
        same_vals = [(k, res[k], exp[k]) for k in dif if res[k] == exp[k]]
        if len(diff_vals) !=0:
            with allure.step(f'断言数据库断言失败字段：{diff_vals}'):
                logger.warning(f'数据库断言失败，数据库查询与期望不一致：{diff_vals}')
            with allure.step(f'断言数据库断言成功字段：{same_vals}'):
                logger.info(f'数据库断言成功字段：{same_vals}')
                # pytest.assume(res[k] == exp[k])
            raise AssertionError(f'断言失败')
        else:
            with allure.step(f'数据库断言成功{exp}与{res}一致'):
                logger.info(f'数据库断言成功{exp}与{res}一致')


if __name__ == '__main__':
    import datetime 
    a = datetime.datetime(2023, 5, 11, 4, 56, 43).strftime('%Y-%m-%d %H:%M:%S')
    b = '2023-05-11T05:48:29.732Z'.replace('T',' ').replace('Z','')[:-4]


    print(datetime.datetime.strptime(b,'%Y-%m-%d %H:%M:%S'))
    
 