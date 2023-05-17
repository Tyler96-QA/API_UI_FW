'''
Author: TylerQA 990687322@qq.com
Date: 2023-04-20 13:42:03
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-04-20 13:56:23
FilePath: \atfx_-ui_framework\tools\handle_tools.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import base64
import json
import time
from functools import wraps
import inspect
import requests
import re
from loguru import logger


#统计某个函数的运行时间
def use_time(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        logger.info(f"函数 {function.__name__} 运行 {'%.2f'%(float(t1-t0))} seconds")
        return result
    return function_timer


#输出运行方法/步骤名
def process_step(function):
    @wraps(function)
    def function_process(*args, **kwargs):
        logger.info('步骤：运行 {} 方法,位于 {} 文件中 {} 行：{}'.format(function.__name__,inspect.getmembers(function)[23][1]+'.py',
        int(re.sub(r'\D',(''.join(re.findall(r'line \d{1,}',str(inspect.getmembers(function)[4][1]))))))+1,inspect.getcomments(function)[1:-1]))
        result = function(*args, **kwargs)
        return result 
    return function_process



"""需要在图鉴网注册账号，注册成功后可使用该接口进行图片识别，另外本地需
下载验证码图片截图，将截图路径放进接口参数中,注册地址：http://www.ttshitu.com/register.html"""
@use_time
def Base64_api(uname:str,pwd:str,img:str,typeid=1003):

    """
    新版本：传入验证码图片路径即可；注意：调用此方法时不要随意移动窗口
    typeid说明：
    一、图片文字类型(默认 3 数英混合)：
    1 : 纯数字
    1001：纯数字2
    2 : 纯英文
    1002：纯英文2
    3 : 数英混合
    1003：数英混合2
    4 : 闪动GIF
    7 : 无感学习(独家)
    11 : 计算题
    1005:  快速计算题
    16 : 汉字
    32 : 通用文字识别(证件、单据)
    66:  问答题
    49 :recaptcha图片识别
    二、图片旋转角度类型：
    29 :  旋转类型
    
    三、图片坐标点选类型：
    19 :  1个坐标
    20 :  3个坐标
    21 :  3 ~ 5个坐标
    22 :  5 ~ 8个坐标
    27 :  1 ~ 4个坐标
    48 : 轨迹类型
    
    四、缺口识别
    18 : 缺口识别（需要2张图 一张目标图一张缺口图）
    33 : 单缺口识别（返回X轴坐标 只需要1张图）
    五、拼图识别
    53：拼图识别
    """
    with open(img, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        b64 = base64_data.decode()
    data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result['success']:
        logger.info(f'验证码识别成功：{result["data"]["result"]}')
        return result["data"]["result"]
    else:
        logger.info(f'验证码识别失败：{result["message"]}')
        return result["message"]
    return ""




#测试
if __name__ == "__main__":
    result = Base64_api('tyler','123456',r'D:\code\tylerhub\demo\public\jietu\Screenshot2022-05-17-15.53.12.png')
    print(result)