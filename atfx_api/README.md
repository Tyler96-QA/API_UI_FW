# ATFX_API

## 介绍
ATFX-API 接口自动化测试

---
## 架构说明

基于python+pytest+requests+allure搭建的接口测试框架

---

## 安装教程

1.  python3.8 版本
2.  安装jdk17+版本，安装allure2.2+版本。配置java、allure环境变量。
3.  依赖包安装：windows命令行pip install -r requirements.txt。*如果本地python环境是3.8+以上版本，可能出现部分依赖包下载失败的问题*，需要手动下载：pip install 包名，下载对应python版本的依赖包。
4.  docker

---
## 目录结构

* ATFX_API
    >根目录
    * data
        >测试用例目录
        * BOS接口用例.xlsx
        * CP接口用例.xlsx
    * imgs
    * logs
    * report
        * allure_report
        * allure_result
    * testcase
        * conftest.py
            >夹具、用例收集器封装
        * test_add_ib_gm.py
        * test_bankWire_withdrawal_gm.py
        * test_bos_send_email.py
        * test_cp_send_email_mu.py
        * test_creditcard_deposit_gm.py
        * test_ewallet_deposit.py
        * test_ewallet_withdrawal_gm.py
        * test_register_mu.py
    * tools
        >公共方法
        * global_SystemEnv.py
            >全局环境变量 
            ```python
            #定义一个全局变量类Environment，将conf.py文件中的环境配置设置为Environment的类属性。执行用例时需要全局共享数据则设置为Environment的类属性，数据分离时导入实例对象SystemEnv设置实例属性
            import os
            import sys
            sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            import conf

            class Environment(object):
                def __new__(cls) -> any:
                    for item in dir(conf):
                        if not item.startswith("__") and not item.endswith("__") and not type(item).__name__ == 'module':
                            setattr(cls,item,getattr(conf,item))
                return cls
            SystemEnv=Environment()
            ```
        * handle_aes.py
            >加密与解密
            ```python
            def encryptData(key:str, iv:str, plaintext:str)->str:
                ...
                return encryp_res
            def decryptData(key:str, iv:str, ciphertext:str)->str:
                ...
                return decrypt_res
            ```
        * handle_assert.py
            >响应结果断言、数据库断言封装，以相等为主，可自行封装其他断言方式，如包含、是与不是、大于等于等等
            >>将从excel中读取的excepted_actions列字符进行占位符替换,字符串转换为字典，字典的每个key都存在于响应体中（**字典中的key与响应体中的必须保持一致**），断言key值是否相等
            ```python
            def assert_resp(resp_dict:dict,excepted_actions:str)->None:
                for ...:
                try:
                    ...
                except:
                    raise AssertionError(f'断言失败：{resp_} 与 {value} 不一致')
            
            def assert_db(assert_db_str:str)->None:
                ...
            ```
        * handle_database.py
            >数据库交互封装：Mysql、MongoDB
            ```python
            def search_in_mongodb(self,uri:str,database:str,muster:str,mongodbserch:dict=None,*args,N:int=0,sortTerm:list=[('_id',-1)])->list:
                """
                读取配置文件中的mongodb链接，传入查询条件查询指定数据库集合中的数据，默认最新数据排序并以列表形式返回
                :param uri:数据库链接
                :param database:数据库
                :param muster:集合
                :param mongodbserch:mongodb查询语句,字典 如{"$and": [{"latdec": 9.3547792}, {"watlev": "always dry"}]}
                :param N:查询条数，默认为0,查询所有
                :param args:需具体查询的字段
                :param sortTerm:是否排序，字典。1升序，-1降序，_id,-1 查询最新数据
                :return 以列表类型返回查询数据
                """
                ...
            def search_in_mysql(self,mysql:str,sql:str,many:int=1)->list:
                """
                默认返回一条数据:dict,返回多条数据：list
                :param mysql :数据库名称
                :param sql: 执行查询的sql语句
                :param many: many:1,返回一条数据；-1返回所有查询数据；>1返回对应条数
                :param return:返回查询数据
                """
                ...
            ```
        * handle_email.py
            >邮件发送服务
            >>收发件人信息配置在conf.py
            ```python
            class SendEmail(object):
                def __init__(self):
                    ...
                def send(self,content:any,form:str,object:str):
                    ...
            ```
        * handle_excel.py
            >读取excel中的测试数据，并将每条用例以类属性的形式保持在Case类中
            ```python
            class Case(object):
            """
            存储测试数据的类
            """
            def __init__(self,attrs:zip) -> None:
                """
                初始化用例
                :param attrs : zip对象
                """
                for item in attrs:
                    setattr(self,item[0],item[1]) #set实例对象的属性
            
            class HandleExcel(object):
                def __init__(self,filename:str,sheetname:str='Sheet1') -> None:
                    ...
                def __del__(self)->None:
                    ...
                def read_excel_data(self)->list:
                    ...
                def read_excel_data_obj(self)->object:
                    ... 
                    case_obj=Case(list(zip(head_list,data_list)))
                    ...
            ```
        * handle_extract.py
            >通过jsonpath表达式从响应结果中提取数据，并设置为全局变量
            ```python
            def handleExtract(extract_str:str,resp_data:dict)->None:
                for ...:
                    if ...:
                    else:
                        raise AttributeError('响应提取失败') 
            ```
        * handle_gen_data.py
            >替换excel数据中的占位符，***函数名要与占位符一致才能成功替换***
            >>新增方法时，需要将方法名添加至映射关系列表__all__中
            ```python
            #指定对外开放的函数,字符串与函数的映射
             __all__ = ['gen_cur_time',...]
            
            def gen_cur_time()->str:
                return str(int(time.time()*1000))
            def ...
            ```
        * handle_image_captcha.py
            >识别二进制验证码图片，并调用三方接口识别验证码
            >>处理逻辑：将接口返回的svg转换成png并保存，调用图鉴网接口识别验证码
            ```python
            def verify_img_code(data:requests.Response)->None:
                try:
                    #svg转png
                    renderPM.drawToFile(svg2rlg(os.path.join(SystemEnv.IMGS_DIR,'svg_code.svg')),os.path.join(SystemEnv.IMGS_DIR,'svg_code.png'))
                    
                    img_code = Base64_api(SystemEnv.TUJIAN_USERNAME,SystemEnv.TUJIAN_PSWORD,os.path.join(SystemEnv.IMGS_DIR,'svg_code.png'),SystemEnv.TUJIAN_TYPE)
                except:
                    ...
            ```
        * handle_log.py
            >日志文件封装，py3.8+以上版本已弃用，其他py版本可调用此模块进行日志的处理
        * handle_pre_sql.py
            >前置SQL处理,excle列中sql字段内容。可以是查询操作，也可以是更改操作
            ```python
            def exeure_sql_set_gobalattr(sql_str:str)->None:
                """
                执行前置sql语句，如果是查询操作，那么将查询的值设置为全局变量
                全局变量名与查询sql语句中select后面的字段名保持一致;或者与field字段的列表元素保持一致
                :param sql_str :excel中sql列的值
                :param return :
                """
                ...
            ```
        * handle_replace_mark.py
            >替换excel中的占位符,占位符数据来源可以是全局变量（数据库读取的值，conf.py中的配置，响应体提取的值），也可以是内置方法（handle_gen_data.py模块中的方法）
            >>根据正则表达式提取excel中读取字符串并按原始顺序返回非重列表，#key#替换成真实的值
            >>>当前封装的正则表达式默认为#(\w+)#，excel中用#key#进行占位。***可自定义占位符格式但同时需要更改正则表达式默认设置。***
            ```python
            def replace_mark_by_data(req_str:str,pattern:str='#(\w+)#')->str:
                
                to_be_replaced_mark = sorted(list(set(mark_list)),key=mark_list.index) #去重列表并不打乱原有的排序
                ...
            ```
        * handle_reponse.py
            >对响应体数据的封装
            >>响应体转换为字典
            >>响应体需要解密
            ```python
            def change_resp_to_dict(resp_decrypt:str,resp:requests.Respones)->dict:
                try:...
                except:...
                #解密
                if resp_decrypt:
                    decrypt_str = decryptData(SystemEnv.VUE_APP_API_ENCRYPT_KEY,SystemEnv.VUE_APP_API_ENCRYPT_IV,resp_dict['data'])
                    resp_dict['data'] = js.loads(decrypt_str)
                return resp_dict
            ```
        * handle_requests.py
            >封装基于项目特色的请求
            >>读取excel请求体字符串后的处理，字符串转换字典后通过requests库发送请求
            >>token鉴权及headers的处理
            ```python
            class HandelRequests(object):
                session = requests.session()
                @classmethod
                def request(cls,method:str,url:str,json:str=None,data:str=None,files:str=None,params:str=None,token:str=None):
                    ...
            
            def public_request(case:object):
                #请求发送前。对前置sql、请求体处理（字符串的占位符替换，加密等）
                ...
                #发送请求时。对请求头、token鉴权处理
                ...
                #请求发送后。对响应体数据的处理（解密，响应体数据提取等）
                ...
            ```
        * handle_tools.py
            >其他工具
            >>图片验证码识别方法封装在此模块中，具体识别类型请看注释。图鉴网账号密码配置在conf.py
            ```python
            #统计函数的运行时间
            def use_time(function):
                @wraps(function)
                def function_timer(*args, **kwargs):
                    ...
            
            #输出运行方法/步骤名
            def process_step(function):
                @wraps(function)
                def function_process(*args, **kwargs):
            
            #识别图片验证码
            @use_time
            def Base64_api(uname:str,pwd:str,img:str,typeid=1003):
                ...
            ```
    * conf.py
        >全局环境变量配置
    * environment.xml
    * main.py
        >项目主入口，可根据mark标记运行用例。并根据插件ordering重新排序用例执行顺序
    * pytest.ini
        >pytest配置文件
    * requirements.txt
        >项目依赖包及版本
    * set_env.py
        >其他虚拟环境的终端配置

---
#### 参与贡献

1.  Fork 本仓库
2.  新建主分支master
3.  提交代码
4.  新建 Pull Request


#### BUG链接

