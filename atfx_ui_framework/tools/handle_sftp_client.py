'''
Author: Tyler Tang tyler.tang@6317.io
Date: 2022-06-14 11:00:19
LastEditors: Tyler96-QA 1718459369@qq.com
LastEditTime: 2023-02-24 10:39:42
FilePath: \tylerhub\demo\public\sftp_client.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os
import re
import pysftp
import urllib.parse
import posixpath
from handlelog import MyLog
from config_manager import get_value

class SFTP():
    def __init__(self):
        self.sftp_host=get_value('SFTP_HOST')
        self.sftp_user=get_value('SFTP_USER')
        self.sftp_passwd=get_value('SFTP_PWD')
        self.root_path=get_value('ROOT_PATH')
        self.remote_root_path=posixpath.join('data','qa_autotest')
        self.remote_write_path=posixpath.join(get_value('BB_PROJECT_NAME',''),'build',get_value('BB_BUILD_NUMBER',''))
        #self.remote_dir=posixpath.join(self.remote_root_path,self.remote_write_path)
        self.file_base_name='index.html'

    def get_report_number(self,build_number_dir_list):
        if not build_number_dir_list:
            return '1'
        try:
            number_filter_list=list(filter(lambda x:x.isdigit(),build_number_dir_list))
            return str(max([int(x) for x in number_filter_list])+1)
        except Exception:
            return '1'
            

    def upload(self,local_path_list:list,description_list:list):
        try:
            # cnopts.hostkeys.load('/root/.ssh/known_hosts')
            with pysftp.Connection(host=self.sftp_host,\
                                username=self.sftp_user,\
                                password=self.sftp_passwd) as sftp:
                print('Connection successfully established...')
                for fru in range(0,len(local_path_list)):
                    self.remote_dir=posixpath.join(self.remote_root_path,self.remote_write_path)
                    sftp.makedirs(self.remote_dir) 
                    report_number=self.get_report_number([x for x in sftp.listdir(self.remote_dir) \
                                                    if sftp.isdir(posixpath.join(self.remote_dir,x))])
                    self.remote_dir = posixpath.join(self.remote_dir,report_number)
                    print('创建服务器远程路径：{}'.format(self.remote_dir))
                    sftp.mkdir(self.remote_dir)
                    print('本地路径为：{}'.format(local_path_list[fru]))
                    if os.path.isdir(local_path_list[fru]):
                        print('远程路径为：{}\n'.format(self.remote_dir))
                        sftp.put_r(local_path_list[fru],self.remote_dir)
                    else:
                        self.file_base_name=os.path.basename(local_path_list[fru])
                        remote_file_path=posixpath.join(self.remote_dir,self.file_base_name)
                        print('远程路径为：{}\n'.format(remote_file_path))
                        sftp.put(local_path_list[fru],remote_file_path)
                    report_http_url = urllib.parse.urljoin(get_value('REPORT_HTTP_URL'),posixpath.join(self.remote_write_path,report_number,self.file_base_name))
                    self.__append_log(description_list[fru],report_http_url)
            print('Upload complete')
        except Exception as msg:
            MyLog().my_logger('------------Sftp exception log---------------\n').error(msg)
        

    def __append_log(self,description,report_http_url):
        with open(os.path.join(self.root_path,'report_list.txt'),'a') as f:
            f.write(description+' '+report_http_url+'\n')