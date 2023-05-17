'''
Author: Tyler Tang tyler.tang@6317.io
Date: 2022-05-05 23:59:38
LastEditors: Tyler Tang tyler.tang@6317.io
LastEditTime: 2022-11-24 16:52:59
FilePath: \at-bos-ui-test\demo\public\ms_teams.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os,pymsteams,sys
from config_manager import load_conf,get_value


class MsTeamsBot():
    def __init__(self):
        load_conf()
        self.report_list_path=os.path.join(get_value('ROOT_PATH'),'report_list.txt')
        
        with open(self.report_list_path,'r') as f:
            lines=f.readlines()
        
        if lines:  
            if divmod(len(lines), 9)[1]==0:
                self.x=divmod(len(lines), 9)[0]
            else:
                self.x=divmod(len(lines), 9)[0]+1
            
        self.title="主人们，由{0} 的 {1} 分支触发的UI自动化测试报告已经生成。".format(\
                    get_value('BB_PROJECT_NAME'),get_value('BB_BRANCH'))
        self.summary='UI AutoTest Detail'


    def send_section(self):
        build_num_text=''
        if get_value('BB_TRIGGER_BUILD_NUMBER'):
            build_num_text=build_num_text+'source_build_num:{0} \t'.format(get_value('BB_TRIGGER_BUILD_NUMBER'))
        if get_value('BB_BUILD_NUMBER'):
            build_num_text=build_num_text+'build_num:{0} \t'.format(get_value('BB_BUILD_NUMBER'))
        section_text="###  {0} \n".format(build_num_text)
        try:
            for i in range(self.x): #生成多个循环变量
                locals()['msteams_bot'+str(i)]=pymsteams.connectorcard(get_value('MSTEAMS_WEBHOOK'))
                locals()['msteams_bot'+str(i)].title(self.title)
                locals()['msteams_bot'+str(i)].summary(self.summary)
                locals()['msteams_bot'+str(i)].color('00FF00')
                locals()['msteams_bot'+str(i)].addSection(pymsteams.cardsection().text(section_text))
            
            with open(self.report_list_path,'r') as f:
                lines=f.readlines()
                
            if lines:
                list1=[]
                n=9 #九条报告为一组
                for y in range(0, len(lines),n):
                    name = lines[y:y + n]
                    list1.append(name)
            
            for i in range(self.x):
                for line in list1[i]:
                    feture_name=line.split(' ')[0]
                    feture_report_url=line.split(' ')[1]
                    section_text="### 测试流程名称 : {0} \n> 测试报告url : [{1}]({2})"\
                    .format(feture_name,feture_report_url,feture_report_url)
                    locals()['msteams_bot'+str(i)].addSection(pymsteams.cardsection().text(section_text))
                locals()['msteams_bot'+str(i)].send()
        except Exception as msg:
            print(f'请检查report_list是否存在内容：{msg}')

if __name__ == '__main__':
    ms_teams_bot=MsTeamsBot()
    ms_teams_bot.send_section()