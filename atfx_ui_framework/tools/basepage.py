

from selenium.webdriver.support import expected_conditions as EC
from loguru import logger
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import inspect
import time
import os
from global_SystemEnv import SystemEnv


class BasePage(object):

    def __init__(self,driver:WebDriver,timeout:int=30,step=0.5) -> None:
        self.driver = driver
        self.timeout = timeout
        self.step = step
        self.wait = WebDriverWait(self.driver, self.timeout,self.step)

    #打开网页
    def open(self,url:str):
        """
        :param url: 要访问的url
        """
        logger.info(f'访问：{url}')
        try:
            self.driver.get(url)
        except BaseException as msg:
            logger.exception('打开页面失败,报错步骤：{}; 报错原因：{}; 报错文件：{}; 报错行数：{}'
            .format(inspect.currentframe().f_back.f_code.co_name,msg,inspect.stack()[1][0].f_code.co_filename,inspect.currentframe().f_back.f_lineno)) 
            raise    

    #查找可见元素，取唯一值
    def find_element_visibility(self,locator:tuple,page_actions:str,index=1)->object:
        """
        元素可见以后查找元素
        :param locator:定位方式，元祖
        :param index:元素在页面上位于第几
        :param page_actions:页面操作
        :return 返回一个元素对象
        """
        try:
            logger.info(f'{page_actions}：等待元素【{locator}】可见,可显示且宽和高都大于0')
            self.wait.until(EC.visibility_of_any_elements_located(locator))
            logger.info(f'查找元素【{locator}】在页面DOM树上的第{index}个')
            ele = self.driver.find_elements(*locator)[index-1]
            return ele
        except BaseException as msg:
            logger.exception('页面操作：{} 失败，报错步骤：{}; 报错原因：{}; 报错文件：{}; 报错行数：{}'
            .format(page_actions,inspect.currentframe().f_back.f_code.co_name,msg,inspect.stack()[1][0].f_code.co_filename,inspect.currentframe().f_back.f_lineno))
            self.save_pageshots(page_actions)
            raise   
    
    #查找元素，取唯一值
    def find_element_presence(self,locator:tuple,page_actions:str,index=1)->object:
        """
        查找元素加载DOM树以后查找元素
        :param locator:定位方式，元祖
        :param index:元素在页面上位于第几
        :param page_actions:页面操作
        :return 返回一个元素对象
        """
        try:
            logger.info(f'{page_actions}：等待元素【{locator}】被加到了dom树里，并不代表该元素一定可见，如果定位到就返回元素')
            self.wait.until(EC.presence_of_all_elements_located(locator))
            ele = self.driver.find_elements(*locator)[index-1]
            logger.info(f'查找元素【{locator}】在页面DOM树上的第{index}个')
            return ele
        except BaseException as msg:
            logger.exception('页面操作：{} 失败，报错步骤：{}; 报错原因：{}; 报错文件：{}; 报错行数：{}'
            .format(page_actions,inspect.currentframe().f_back.f_code.co_name,msg,inspect.stack()[1][0].f_code.co_filename,inspect.currentframe().f_back.f_lineno))
            self.save_pageshots(page_actions)
            raise  
    
    #点击元素
    def click_element(self,locator:tuple,page_actions:str,index=1):
        """
        点击元素
        :param locator:定位方式，元祖
        :param index:元素在页面上位于第几个
        :param page_actions:页面操作 
        """
        ele = self.find_element_visibility(locator,page_actions,index)  
        try:
            logger.info(f'点击元素：【{locator}】在DOM树上的第{index}个')
            ele.click()
        except BaseException as msg:
            logger.exception('页面操作：{} 失败，报错步骤：{}; 报错原因：{}; 报错文件：{}; 报错行数：{}'
            .format(page_actions,inspect.currentframe().f_back.f_code.co_name,msg,inspect.stack()[1][0].f_code.co_filename,inspect.currentframe().f_back.f_lineno))
            self.save_pageshots(page_actions)
            raise 
    
    #输入
    def input_value(self,locator:tuple,value:str,page_actions:str,index=1,clear=True):
        """
        输入
        :param locator:定位方式，元祖
        :param index:元素在页面上位于第几个
        :param clear:输入框是否需要清除原始内容
        :param page_actions:页面操作 
        """
        ele = self.find_element_visibility(locator,page_actions,index)
        try:
            if clear:
                logger.info(f'清除元素【{locator}】位于DOM树上第{index}个的文本内容')
                ele.clear()
            logger.info(f'执行输入操作，输入：{value}')
            ele.send_keys(value)
        except BaseException as msg:
            logger.exception('页面操作：{} 失败，报错步骤：{}; 报错原因：{}; 报错文件：{}; 报错行数：{}'
            .format(page_actions,inspect.currentframe().f_back.f_code.co_name,msg,inspect.stack()[1][0].f_code.co_filename,inspect.currentframe().f_back.f_lineno))
            self.save_pageshots(page_actions)
            raise 

    def input_imgs(self,locator:tuple,value:str,page_actions:str,index=1):
        ele = self.find_element_presence(locator,page_actions,index)
        try:
            ele.send_keys(value)
            logger.info(f'上传图片：{value}')
        except BaseException as msg:
            logger.exception('页面操作：{} 失败，报错步骤：{}; 报错原因：{}; 报错文件：{}; 报错行数：{}'
            .format(page_actions,inspect.currentframe().f_back.f_code.co_name,msg,inspect.stack()[1][0].f_code.co_filename,inspect.currentframe().f_back.f_lineno))
            self.save_pageshots(page_actions)
            raise         
    
    #获取元素文本
    def get_text(self,locator:tuple,page_actions:str,index=1)->str:
        """
        获取元素文本
        :param locator:定位方式，元祖
        :param index:元素在页面上位于第几个
        :param page_actions:页面操作 
        """ 
        ele = self.find_element_visibility(locator,page_actions,index)     
        try:
            value = ele.text
            logger.info(f'获取元素：【{locator}】文本，位于DOM树上第 {index} 个，返回的文本信息为：{value}')
            return value
        except BaseException as msg:
            logger.exception('页面操作：{} 失败，报错步骤：{}; 报错原因：{}; 报错文件：{}; 报错行数：{}'
            .format(page_actions,inspect.currentframe().f_back.f_code.co_name,msg,inspect.stack()[1][0].f_code.co_filename,inspect.currentframe().f_back.f_lineno))
            self.save_pageshots(page_actions)
            raise   

    #获取元素属性
    def get_attribute(self,locator:tuple,attr_name:str,page_actions:str,index=1)->str:
        """
        获取元素属性
        :param locator:定位方式，元祖
        :param attr_name:元素
        :param index:元素在页面上位于第几个
        :param page_actions:页面操作 
        """ 
        ele = self.find_element_presence(locator,page_actions,index)     
        try:
            value = ele.get_attribute(attr_name)
            logger.info(f'获取元素：【{attr_name}】的属性，位于DOM树上第 {index} 个，返回的属性值为：{value}')
            return value
        except BaseException as msg:
            logger.exception('页面操作：{} 失败，报错步骤：{}; 报错原因：{}; 报错文件：{}; 报错行数：{}'
            .format(page_actions,inspect.currentframe().f_back.f_code.co_name,msg,inspect.stack()[1][0].f_code.co_filename,inspect.currentframe().f_back.f_lineno))
            self.save_pageshots(page_actions)
            raise      
    
    #判断某个元素是否可见
    def ele_is_display(self,locator):
        try:
           WebDriverWait(self.driver,2,0.5).until(EC.presence_of_all_elements_located(locator))
           return True
        except:
            return False
        
    def ele_is_visibility(self,locator):
        try:
           WebDriverWait(self.driver,1,0.5).until(EC.visibility_of_element_located(locator))
           return True
        except:
            return False
  
    #鼠标悬停
    def mouse_suspend(self,locator:tuple,page_actions:str,index=1):
        """
        鼠标悬浮，过程中请不要移动鼠标
        :params locator:定位方式，元祖
        :param index:元素在页面上位于第几个
        :param page_actions:页面操作        
        """
        ele = self.find_element_visibility(locator,page_actions,index)
        try:
            logger.info(f'鼠标悬浮至元素：【{locator}】，位于DOM树上的第{index}个')
            ActionChains(self.driver).move_to_element(ele).perform()
        except BaseException as msg:
            logger.exception('页面操作：{} 失败，报错步骤：{}; 报错原因：{}; 报错文件：{}; 报错行数：{}'
            .format(page_actions,inspect.currentframe().f_back.f_code.co_name,msg,inspect.stack()[1][0].f_code.co_filename,inspect.currentframe().f_back.f_lineno))
            self.save_pageshots(page_actions)
            raise       
    
    #双击
    def double_click(self,locator:tuple,page_actions:str,index=1):
        """
        鼠标双击
        :params locator:定位方式，元祖
        :param index:元素在页面上位于第几个    
        :param page_actions:页面操作      
        """
        ele = self.find_element_visibility(locator,page_actions,index)
        try:
            logger.info(f'双击元素：【{locator}】，位于DOM树上的第{index}个')
            ActionChains(self.driver).double_click(ele).perform()
        except BaseException as msg:
            logger.exception('页面操作：{} 失败，报错步骤：{}; 报错原因：{}; 报错文件：{}; 报错行数：{}'
            .format(page_actions,inspect.currentframe().f_back.f_code.co_name,msg,inspect.stack()[1][0].f_code.co_filename,inspect.currentframe().f_back.f_lineno))
            self.save_pageshots(page_actions)
            raise     
    
    #右键点击
    def ringht_click(self,locator:tuple,page_actions:str,index=1):
        """
        右键点击
        :params locator:定位方式，元祖
        :param index:元素在页面上位于第几个
        :param page_actions:页面操作          
        """
        ele = self.find_element_visibility(locator,page_actions,index)
        try:        
            logger.info('右键点击元素：【{locator}】，位于DOM树上的第：{index}个')
            ActionChains(self.driver).context_click(ele).perform()
        except BaseException as msg:
            logger.exception('页面操作：{} 失败，报错步骤：{}; 报错原因：{}; 报错文件：{}; 报错行数：{}'
            .format(page_actions,inspect.currentframe().f_back.f_code.co_name,msg,inspect.stack()[1][0].f_code.co_filename,inspect.currentframe().f_back.f_lineno))
            self.save_pageshots(page_actions)
            raise          
    

    #其他键盘操作(针对搜索框/输入框)
    def keyboard_operation(self,locator:tuple,keys:str,page_actions:str,index=1):
        """
        键盘操作
        :param locator:元素定位元祖
        :param keys:a,全选;c:粘贴;v:复制；x:剪切
        :param page_actions:页面操作 
        """
        ele = self.find_element_visibility(locator,page_actions,index)
        try:
            ele.send_keys(Keys.CONTROL,keys)
            logger.info(f'在输入框中执行 ctrl+{keys} 操作')
        except BaseException as msg:
            logger.exception('页面操作：{} 失败，报错步骤：{}; 报错原因：{}; 报错文件：{}; 报错行数：{}'
            .format(page_actions,inspect.currentframe().f_back.f_code.co_name,msg,inspect.stack()[1][0].f_code.co_filename,inspect.currentframe().f_back.f_lineno))
            self.save_pageshots(page_actions)
            raise 
   
    #切换窗口
    def switch_windows(self,n:int,page_actions:str):
        """
        切换窗口
        :params n:切换到第n个窗口,窗口列表下标
        :param page_actions:页面操作 
        """
        try:
            wins = self.driver.window_handles
            logger.info(f'切换到窗口列表的第{n}个:{page_actions}')
            self.driver.switch_to.window(wins[n])
        except BaseException as msg:
            logger.exception('页面操作：{} 失败，报错步骤：{}; 报错原因：{}; 报错文件：{}; 报错行数：{}'
            .format(page_actions,inspect.currentframe().f_back.f_code.co_name,msg,inspect.stack()[1][0].f_code.co_filename,inspect.currentframe().f_back.f_lineno))
            self.save_pageshots(page_actions)
            raise 

    #切换iframe
    def switch_into_iframe(self, iframe_loc, page_action ):
        """
        切换iframe
        :param iframe_loc: index, id或者name属性的值，元素定位元组。
        :return:
        """
        logger.info(f"切换进入iframe: {iframe_loc}")
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.frame_to_be_available_and_switch_to_it(iframe_loc))
        except BaseException as msg:
            logger.exception('页面操作：{} 失败，报错步骤：{}; 报错原因：{}; 报错文件：{}; 报错行数：{}'
            .format(page_action,inspect.currentframe().f_back.f_code.co_name,msg,inspect.stack()[1][0].f_code.co_filename,inspect.currentframe().f_back.f_lineno))
            self.save_pageshots(page_action)
            raise 

    #失败截图
    def save_pageshots(self, page_actions:str)->None:
        # 截图命名可以快速找到 业务名称_时间戳.png
        cur_time = time.strftime("%Y%m%d", time.localtime())
        file_name = f"{page_actions}失败_{cur_time}.png"
        file_path = os.path.join(SystemEnv.ERRORIMGS_DIR,file_name)
        self.driver.save_screenshot(file_path)
        logger.info(f"页面截图保存在：{file_path}")

    #根據元素定位截圖
    def elementImage(self,locator:tuple,page_actions:str,index=1)->str:
        """
        元素定位截图
        :param locator:元素定位，元祖
        :param index:元素在页面上位于第几个
        :param page_actions:页面操作
        """
        ele = self.find_element_visibility(locator,page_actions,index)
        try:
            pict_name=time.strftime('%Y%m%d-%H%M',time.localtime(time.time()))+f'{page_actions}.png'
            pic_path = os.path.join(SystemEnv.ELEIMGS_DIR,pict_name)
            logger.info(f'根据元素定位：【{locator}】定点截图')
            ele.screenshot(pic_path)
            return pic_path
        except BaseException as msg:
            self.save_pageshots(page_actions)
            logger.exception('页面操作：{} 失败，报错步骤：{}; 报错原因：{}; 报错文件：{}; 报错行数：{}'
            .format(page_actions,inspect.currentframe().f_back.f_code.co_name,msg,inspect.stack()[1][0].f_code.co_filename,inspect.currentframe().f_back.f_lineno))
            raise 

    #元素聚焦
    def element_focus(self,locator:tuple,page_actions:str,index=1)->str:
        """
        将页面滑动至元素出现的位置
        :param locator:元素定位，元祖
        :param index:元素在页面上位于第几个
        :param page_actions:页面操作
        """ 
        ele = self.find_element_visibility(locator,page_actions,index)      
        try:
            logger.info(f'将页面滑动至元素：【{locator}】可见的位置')
            self.driver.execute_script("arguments[0].scrollIntoView();",ele)
        except BaseException as msg:
            logger.exception('页面操作：{} 失败，报错步骤：{}; 报错原因：{}; 报错文件：{}; 报错行数：{}'
            .format(page_actions,inspect.currentframe().f_back.f_code.co_name,msg,inspect.stack()[1][0].f_code.co_filename,inspect.currentframe().f_back.f_lineno))
            self.save_pageshots(page_actions)
            raise 

    #js修改元素属性
    def js_change_attr(self,locator:tuple,attr:str,value:str,page_actions:str,index=1):
        """
        js更改页面属性的值
        :param locator:元素定位，元祖
        :param page_actions:页面操作
        :param index:元素在页面上位于第几个
        :param attr:要修改的属性
        :param value:修改的值
        """
        ele = self.find_element_presence(locator,page_actions,index)
        try:
            js = f'arguments[0].{attr}="{value}";'
            logger.info(f'更改页面 {attr}属性 的值为 {value}')
            self.driver.execute_script(js,ele)
        except BaseException as msg:
            self.save_pageshots(page_actions)
            logger.exception('页面操作：{} 失败，报错步骤：{}; 报错原因：{}; 报错文件：{}; 报错行数：{}'
            .format(page_actions,inspect.currentframe().f_back.f_code.co_name,msg,inspect.stack()[1][0].f_code.co_filename,inspect.currentframe().f_back.f_lineno))
            raise

    #JS处理滚动条
    def js_top_or_down(self,page_actions:str,size=10000):
        """
        js控制页面滚动
        :param size:1000顶部，0：顶部；其他；
        """
        try:
            if size == 0:
                js = f"document.documentElement.scrollTop={size};"
                logger.info('将页面滚动到顶部')
            else:
                logger.info('将页面滚动到底部')
                js = f"document.documentElement.scrollTop={size};"
            self.driver.execute_script(js)
        except BaseException as msg:
            logger.exception('页面操作：{} 失败，报错步骤：{}; 报错原因：{}; 报错文件：{}; 报错行数：{}'
            .format(page_actions,inspect.currentframe().f_back.f_code.co_name,msg,inspect.stack()[1][0].f_code.co_filename,inspect.currentframe().f_back.f_lineno))
            self.save_pageshots(page_actions)
            raise   
    
    
    #js控制内嵌滚动条
    def js_inside_scroll(self,element:str,page_actions,index=0,size=10000,type='Class'):
        """
        js处理内嵌滚动条

        """
        try:
            logger.info(f'{page_actions}')
            if type == 'ID':
                js=f"""document.getElementsById("{element}")[{index}].scrollTop = {size};"""
            else:    
                js=f"""document.getElementsByClassName("{element}")[{index}].scrollTop={size};"""
            self.driver.execute_script(js)
        except BaseException as msg:
            self.save_pageshots(page_actions)
            logger.exception('页面操作：{} 失败，报错步骤：{}; 报错原因：{}; 报错文件：{}; 报错行数：{}'
            .format(page_actions,inspect.currentframe().f_back.f_code.co_name,msg,inspect.stack()[1][0].f_code.co_filename,inspect.currentframe().f_back.f_lineno))
            raise     
    
    #JS新开窗口
    def js_openwindows(self,url:str):
        logger.info(f'js新开窗口访问：{url}')
        js = 'window.open("{}")'.format(url)
        self.driver.execute_script(js)

    #判断元素是否被勾选
    def is_selectde(self,locator:tuple,page_actions:str,index=1)->bool:
        """
        判断元素是否被勾选
        :param locator:元素定位，元祖
        :param page_actions:页面操作 
        :param index:元素在页面上位于第几个 
        """
        ele = self.find_element_visibility(locator,page_actions,index)
        try:
            logger.info(f'判断元素【{locator}】是否被勾选')
            result = self.wait.until(EC.element_to_be_selected(ele))
            #result = ele.is_selected()
            logger.info(f'元素【{locator}】是否被勾选 :{result}')
            return result
        except BaseException as msg:
            self.save_pageshots(page_actions)
            logger.exception('页面操作：{} 失败，报错步骤：{}; 报错原因：{}; 报错文件：{}; 报错行数：{}'
            .format(page_actions,inspect.currentframe().f_back.f_code.co_name,msg,inspect.stack()[1][0].f_code.co_filename,inspect.currentframe().f_back.f_lineno))
            raise 

    #获取页面title
    def get_title(self)->str:
        return self.driver.title

    #后退
    def driver_back(self):
        self.driver.back()   

    #刷新
    def driver_refresh(self):
        self.driver.refresh()
    
    #关闭当前页
    def close_browser(self):
        self.driver.close()

    #退出浏览器进程
    def quit_browser(self):
        self.driver.quit() 