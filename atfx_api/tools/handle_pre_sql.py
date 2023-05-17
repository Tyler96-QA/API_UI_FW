'''
Author: Tyler96-QA 1718459369@qq.com
Date: 2023-04-13 16:03:42
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-05-11 01:55:08
FilePath: \Api_test\api_framework_v1\tools\handle_pre_sql.py
Description: 执行前置sql语句，excle列中sql字段内容。可以是查询操作，也可以是更改操作
'''
from handle_replace_mark import replace_mark_by_data
from handle_database import DatabaseOperate
from global_SystemEnv import SystemEnv
from loguru import logger
import allure,re

handle_database = DatabaseOperate()

@allure.step('处理前置sql,判断sql中是否有要替换的mark')
def exeure_sql_set_gobalattr(sql_str:str)->None:
    """
    执行前置sql语句，如果是查询操作，那么设置为全局变量
    全局变量名与查询sql语句中select后面的字段名保持一致;或者与field字段的列表元素保持一致
    :param sql_str :excel中sql列的值
    :param return :
    """
    pattern = r'\{.*?\]}'
    reslist= re.findall(pattern,sql_str)
    if reslist:
        logger.info(f'查询 {len(reslist)} 个前置sql：')
        if len(reslist) == 1:#单个mongodb查询。
            sql_new = replace_mark_by_data(sql_str)
            sql = eval(sql_new)
            dict_data = handle_database.search_in_mongodb(SystemEnv.MONGODB.get('uri'),
                                                        sql.get('database'),
                                                        sql.get('muster'),
                                                        sql.get('sql'),
                                                        *sql.get('field'),
                                                        N=1) #返回一条数据
            for key,value in dict_data[0].items():
                with allure.step(f'将数据库读取的数据作为全局变量：{key} : {value}'):
                    setattr(SystemEnv,key,value)
                    logger.info(f'设置的全局变量为：{key}，值：{value}')
        else:#多个mongodb查询。
            for i in reslist:
                sql_new = replace_mark_by_data(i)
                sql = eval(sql_new)
                dict_data = handle_database.search_in_mongodb(SystemEnv.MONGODB.get('uri'),
                                                              sql.get('database'),
                                                              sql.get('muster'),
                                                              sql.get('sql'),
                                                              *sql.get('field'),
                                                              N=1) #返回一条数据
                for key,value in dict_data[0].items():
                    with allure.step(f'将数据库读取的数据作为全局变量：{key} : {value}'):
                        setattr(SystemEnv,key,value)
                        logger.info(f'设置的全局变量为：{key}，值：{value}')
    else:
        #执行sql
        if sql_str.upper().startswith('SELECT') or sql_str.upper().startswith('INSERT') or sql_str.upper().startswith('DELETE'):
            dict_data = handle_database.search_in_mysql(sql=sql_str,many=1) #默认返回一条数据
            for key,value in dict_data.items():
                setattr(SystemEnv,key,value)
                with allure.step(f'将数据库读取的数据作为全局变量：{key}:{value}'):
                    logger.info(f'设置的全局变量为：{key}，值：{value}')
        else:
            logger.info('执行数据库更新操作')
            with allure.step('执行数据库更新操作'):
                handle_database.modify_mysql('MYSQL',sql=sql)

if __name__ == '__main__':
    SystemEnv.eWalletName = 'Skrill'
    sql_str = """{'database':'atfx-#ENVIRONMENT#','muster':'bos_psp_currency','sql':{'pspId':'#eWalletName#'.lower()},'field':['currency']}"""
    exeure_sql_set_gobalattr(sql_str)

