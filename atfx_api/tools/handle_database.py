'''
Author: tyler
Date: 2021-08-26 18:27:17
LastEditTime: 2023-05-12 16:49:24
LastEditors: TylerQA 990687322@qq.com
Description: Query database and save
FilePath: \tylerhub\demo\public\handle_database.py
'''

import pymongo
import ssl
import pymysql
import inspect
from handle_excel import HandleExcel
from handle_tools import use_time
from loguru import logger
from global_SystemEnv import SystemEnv

#全局取消证书验证
ssl._create_default_https_context=ssl._create_unverified_context()

#添加oracle驱动程序(添加驱动后系统找不到allure程序/系统无法同时运行两个驱动程序)
#config_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'config')
# os.environ['path']=os.path.join(config_path,'instantclient_19_11')


class DatabaseOperate(object):
    """
    mysql,oracle,mongodb数据库查询与保存
    """

    #连接mongodb数据库查询数据
    @use_time #统计查询时间
    def search_in_mongodb(self,uri:str,database:str,muster:str,mongodbserch:dict=None,*args,N:int=0,sortTerm:list=[('_id',-1)])->list:
        """
        读取配置文件中的mongodb链接，传入查询条件查询指定数据库集合中的数据，默认最新数据排序并以列表形式返回
        :param uri:数据库链接
        :param database:数据库
        :param muster:集合
        :param mongodbserch:mongodb查询语句,字典,类似于sql语句 如{"$and": [{"latdec": 9.3547792}, {"watlev": "always dry"}]}
        :param N:查询条数，默认为0,查询所有
        :param args:需具体查询的字段
        :param sortTerm:是否排序，字典。1升序，-1降序，_id,-1 查询最新数据
        :return 以列表类型返回查询数据
        """
        logger.info(f'查询mongodb数据库，database：{database}，集合：{muster}，查询字段：{args}')
        #2.0mongodb数据库链接
        try:
            self.client=pymongo.MongoClient(uri,ssl_cert_reqs=ssl.CERT_NONE)
            self.db=self.client[database]
            self.colletion=self.db[muster]
            #查询条件不为空
            if not mongodbserch==None:
                self.list_data=[]
                #查询所有数据
                if N==0:
                    self.data=self.colletion.find(mongodbserch).sort(sortTerm)
                    #查所有字段
                    if len(args)==0:
                        for i in self.data:
                            self.list_data.append(i)
                    #查询指定字段
                    else:
                        for i in self.data:
                            self.dict_search={}
                            for x in args:
                                self.dict_search[x]=i[x]
                            self.list_data.append(self.dict_search)    
                #查询部分数据
                else:
                    self.data=self.colletion.find(mongodbserch).limit(N).sort(sortTerm)
                    #查询所有字段
                    if len(args)==0:
                        for i in self.data:
                            self.list_data.append(i)
                        #查询指定字段
                    else:
                        for i in self.data:
                            self.dict_search={}
                            for x in args:
                                self.dict_search[x]=i[x]
                            self.list_data.append(self.dict_search)   
            #查询条件为空时
            else:
                self.list_data=[]
                #查询所有数据
                if N==0:
                    self.data=self.colletion.find().sort(sortTerm)
                    #查询所有字段
                    if len(args)==0:
                        for i in self.data:
                            self.list_data.append(i)
                    #查询指定字段
                    else:
                        for i in self.data:
                            self.dict_search={}
                            for x in args:
                                self.dict_search[x]=i[x]
                            self.list_data.append(self.dict_search)    
                #查询部分数据
                else:
                    self.data=self.colletion.find().limit(N).sort(sortTerm)
                    #查询所有字段
                    if len(args)==0:
                        for i in self.data:
                            self.list_data.append(i)
                    #查询指定字段
                    else:
                        for i in self.data:
                            self.dict_search={}
                            for x in args:
                                self.dict_search[x]=i[x]
                            self.list_data.append(self.dict_search)    
            logger.info(f'返回数据：{len(self.list_data)}条：{self.list_data}')
            return self.list_data
        except Exception as msg:
            logger.error('\报错步骤：{}; 报错原因：{}; 报错文件：{}; 报错行数：{}'
            .format(inspect.currentframe().f_back.f_code.co_name,msg,inspect.stack()[1][0].f_code.co_filename,inspect.currentframe().f_back.f_lineno)) 
            logger.error('数据库连接或参数有误,请检查用户密码,参数,查询字段或本机ip是否能连接数据库:{}'.format(msg))


    #mongodb数据保存
    @use_time #统计函数运行时间
    def save_mongodb_data(self,excelpath:str,uri:str,database:str,muster:str,mongodbserch:dict=None,N:int=0,sortTerm:list=[('_id',-1)],**kwargs)->str:
        
        """
        :param excelpath:本地文档路径
        :param uri:数据库链接
        :param database:数据库
        :param muster:集合
        :param mongodbserch:mongodb查询语句,字典,类似于sql语句,如{"$and": [{"latdec": 9.3547792}, {"watlev": "always dry"}]}
        :param N:查询条数,默认为0
        :param sortTerm:是否排序,字典。1升序，-1降序，_id,-1 查询最新数据
        :param kwargs:键值对，key对应需查询字段，value对应查询字段保存在本地文档中列，如title='A',runtime='B',rated='C'
        调用save_mongodb_data查询，保存查询数据到本地文档
        """

        try:
            #拆分kwargs参数
            self.list_search=[]
            self.list_save=[]
            #获取key与value值
            for key,value in kwargs.items():
                HandleExcel(excelpath).sava_excel_data(key,1,value)
                self.list_search.append(key)
                self.list_save.append(value)
            #调用函数查询数据库
            self.mongo_data=self.search_in_mongodb(uri, database, muster,mongodbserch,*self.list_search,N=N,sortTerm=sortTerm)
            # #保存数据
            for i in self.list_search:
                for y in self.mongo_data:
                    HandleExcel(excelpath).saveainfo(y[i], self.mongo_data.index(y)+2,self.list_save[self.list_search.index(i)],)

                print('字段"{}"保存在{}列'.format(i,self.list_save[self.list_search.index(i)]))
        except Exception as msg:
            logger.error('\报错步骤：{}; 报错原因：{}; 报错文件：{}; 报错行数：{}'
            .format(inspect.currentframe().f_back.f_code.co_name,msg,inspect.stack()[1][0].f_code.co_filename,inspect.currentframe().f_back.f_lineno)) 
            print('请检查参数及数据库链接是否有误：{}'.format(msg))



    #连接mysql数据库查询
    @use_time #统计函数运行时间
    def search_in_mysql(self,sql:str,many:int=1,mysql:str=None,)->list:
        logger.info('查询mysql数据库........')
        """
        默认返回一条数据:dict,返回多条数据：list
        :param mysql :数据库名称
        :param sql: 执行查询的sql语句
        :param many: many:1,返回一条数据；-1返回所有查询数据；>1返回对应条数
        :param return:返回查询数据
        """
        if mysql:
            self.database = mysql
        else:
            self.database = None
        
        self.host,self.user,self.psword,self.port = [SystemEnv.MYSQL.get(i) for i in ['host','user','password','port']]
        
        try:
            logger.info(f'执行的sql为 : {sql}')
            #连接
            self.db = pymysql.connect(host=self.host,
                                      user=self.user,
                                      password=self.psword,
                                      database=self.database,
                                      port=self.port,
                                      charset='utf8mb4',
                                      cursorclass=pymysql.cursors.DictCursor) #返回列表嵌套字典的结果
            #创建游标对象
            self.cursor=self.db.cursor()
            #执行sql语句
            counts = self.cursor.execute(sql) #此处会生成一个查询结果的条数。
            logger.info(f'执行该sql语句一共查询到{counts}条数据')
            #返回单条数据
            if counts > 0:
                if many==1:
                    self.data=self.cursor.fetchone()
                    count = 1
                #返回*条数据
                elif many > 1:
                    self.data=self.cursor.fetchmany(size=many)
                    count = len(self.data)
                #返回所有数据
                else:
                    self.data=self.cursor.fetchall()
                    count = len(self.data)
                logger.info(f'返回{count}条数据，返回的查询数据为：{self.data}')
                return self.data
            else:
                logger.info('执行该sql在数据中没有查询到数据')
                return None
        except Exception as msg:
            logger.error('\n报错步骤：{}; 报错原因：{}; 报错文件：{}; 报错行数：{}'
            .format(inspect.currentframe().f_back.f_code.co_name,msg,inspect.stack()[1][0].f_code.co_filename,inspect.currentframe().f_back.f_lineno))             
            print('请检查连接信息及sql语句是否正确：{}'.format(msg))
        finally:
                self.cursor.close()
                self.db.close()


    @use_time #统计函数运行时间
    def modify_mysql(self,mysql:str,sql:str)->None:
        """
        默认返回一条数据
        :param mysql :数据库名称
        :param sql: 执行修改数据库的sql语句
        :param many: many:1,返回一条数据；-1返回所有查询数据；>1返回对应条数
        """
        if mysql == 'MYSQL':
            self.database = 'yami_shops'
        else:
            self.database = None
        
        self.host,self.user,self.psword,self.port = [getattr(SystemEnv,mysql).get(i) for i in ['host','user','password','port']]
        try:
            logger.info(f'执行的sql为 : {sql}')
            #连接
            self.db = pymysql.connect(host=self.host,
                                      user=self.user,
                                      password=self.psword,
                                      database=self.database,
                                      port=self.port,
                                      charset='utf8mb4',
                                      cursorclass=pymysql.cursors.DictCursor) #返回字典的形式
            #创建游标对象
            self.cursor=self.db.cursor()
            #执行sql语句
            self.cursor.execute(sql) 
            self.db.commit()
        except:
            self.db.rollback()
        finally:
                self.cursor.close()
                self.db.close()            




#测试
if __name__=='__main__':
    sql = "SELECT MT4_Ref_No,Ticket_No,TYPE,Ticket_No,Entity,Cln_Name,ATNumber,Create_Date,Curr_Status,Fee,UpdateBy,MT4_Account,Bank_Ref_No,Channel,Charge,From_Amt,From_Ccy,Rate,Reason,Remark,Amount,Currency,MT4_Ref_No,COMMENT,Agent,SalesNumber,Close_Date FROM datawarehouse_two_mu_sit.transaction where TYPE='deposit' ORDER BY id desc limit 1;"
    database = DatabaseOperate()
    data_mysql= database.search_in_mysql(sql=sql,many=1)
    data_mongodb = database.search_in_mongodb(SystemEnv.MONGODB.get('uri'),'atfxmu-sit','atfx_deposit',{'accountNumber':1500000243,'tradeAccount':'16300113'},N=1)

#     dataBase=DatabaseOperate()
#     dataBase.search_mysql_dict('SELECT user_mobile FROM tz_user','47.113.180.81','lemon','lemon123',)
    # dataBase.search_in_mongodb(conFig.get_value('mongodb_test', 'uri'), 'sample_mflix', 
    # 'movies',{"year":1915},'title','runtime',N=0)
    # excelpath=r'D:\code\tylerhub\demo\public\about_data.xlsx'
    # dataBase.save_mongodb_data(excelpath,conFig.get_value('mongodb_test', 'uri'),'sample_mflix','movies',
    # {"year":1915},N=0,sortTerm=[('_id',-1)],title='A',runtime='B',rated='C')
    # dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'), 'atfxgm-{}'.format(get_value('ENVIRONMENT')), 'atfx_trade_account',
    # {"accountNumber":1000005349},'tradeAccount',N=1)
    # encrypt_secret=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'), 'atclientpoolsit', 'usersgm',{"email":'tyler.tang@test.com'},'encrypt_secret',N=0)
    # print(encrypt_secret[0]['encrypt_secret'])
    # times=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'),
    # 'atfxgm-{}'.format(get_value('ENVIRONMENT')), 'atfx_deposit',{"currStatus":"S"},'channel',N=0)
    # withdrawal_list=[]
    # for i in range(0,len(times)):
    #     withdrawal_list.append(times[i]['channel'])

    # print(list(set(withdrawal_list)))
    # dataBase.search_in_mongodb(conFig.get_value('mongodb','uri'),'atfxgm-{}'.format(get_value('ENVIRONMENT')),'atfx_account_info',{"accountNumber":1000005349},'lang',N=1)
    # mysql_closeOrder=dataBase.search_in_mysql('SELECT * FROM report_atfx2_test.mt4_sync_order WHERE Login="66200125" and Close_Time!="1970-01-01 00:00:00" order by Ticket',
    #  conFig.get_value('mysql_AWS', 'host'), conFig.get_value('mysql_AWS','user'),conFig.get_value('mysql_AWS','password'),type='all')
    # print(mysql_closeOrder[0][6])
    # lower_withdrawalDatabase=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'),'atfxgm-{}'.format(get_value('ENVIRONMENT')), 'atfx_deposit',
    # {"accountNumber":1000006223},'mtRefNo','accountNumber','tradeAccount','clnName','lastUpdateDate','mt4Amt',N=0,sortTerm=[('_id',1)])
    # print(lower_withdrawalDatabase)	

    # print('544097' in lower_withdrawalDatabase)
    # print(list(dataBase.search_in_mysql('SELECT * FROM report_atfx2_test.mt4_sync_order WHERE Login="{}" and Close_Time="1970-01-01 00:00:00" and'
    # ' Open_Time between "{} 00:00:00" and "{} 23:59:59" order by Open_Time desc'.
    # format(672007722,'2022-03-30','2022-03-30'), conFig.get_value('mysql_AWS', 'host'), conFig.get_value('mysql_AWS','user'),conFig.get_value('mysql_AWS','password'),type='all')))
    
    # print(dataBase.search_in_mysql('SELECT * FROM report_atfx2_test.mt4_sync_order WHERE Login="672007722"',conFig.get_value('mysql_AWS', 'host'),conFig.get_value('mysql_AWS','user'),conFig.get_value('mysql_AWS','password'),type='all'))
    # print(dataBase.search_mysql_dict('SELECT * FROM report_atfx2_test.mt4_sync_order WHERE Login="672006226"',get_value('MYSQL_AWS').get('host'), get_value('MYSQL_AWS').get('user'),get_value('MYSQL_AWS').get('password'),type='all'))
    # mongodbDeposit=dataBase.search_in_mongodb(get_value('MONGODB').get('uri'),
    # 'atfxgm-{}'.format(get_value('ENVIRONMENT')), 'atfx_deposit',{"$and":[{"currStatus":"S"},{"accountNumber": 1000005349}]}
    # ,'createDate','fromAmt','rate','mt4Amt','currStatus','channel',N=0)
    # print(mongodbDeposit)