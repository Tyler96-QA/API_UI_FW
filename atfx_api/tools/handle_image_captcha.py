'''
Author: TylerQA 990687322@qq.com
Date: 2023-04-18 15:56:02
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-05-10 13:13:11
FilePath: \atfx_api\tools\handle_image_captcha.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os 
from loguru import logger
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from global_SystemEnv import SystemEnv
from handle_tools import Base64_api
import allure

@allure.step('识别二进制验证码图片，并调用三方接口识别验证码')
def verify_img_code(data)->None:
    """
    :param data:响应体。接口返回图片，二进制后获取响应的图片信息
    """
    try:
        #得到响应体中的data（svg图片格式），并转换成对应的编码格式保存在本地文件.svg中
        logger.info('将响应体中的data（svg图片格式）转换成对应的编码格式保存在本地文件.svg中')
        
        with open(os.path.join(SystemEnv.IMGS_DIR,'svg_code.svg'),'wb') as f:
            f.write(eval(data.content)['data'].encode()) #将字符串编码后写入svg文件

        #将svg图片转换为png图片
        logger.info('SVG文件转PNG')
        renderPM.drawToFile(svg2rlg(os.path.join(SystemEnv.IMGS_DIR,'svg_code.svg')),os.path.join(SystemEnv.IMGS_DIR,'svg_code.png'))

        logger.info('调用第三方接口识别验证码')
        
        with allure.step('svg转png验证码图片'):
            with open(os.path.join(SystemEnv.IMGS_DIR,'svg_code.png'),'rb') as f: #入金方式截图
                comtent=f.read()
            allure.attach(comtent,'验证码图片',allure.attachment_type.PNG)
        
        img_code = Base64_api(SystemEnv.TUJIAN_USERNAME,SystemEnv.TUJIAN_PSWORD,os.path.join(SystemEnv.IMGS_DIR,'svg_code.png'),SystemEnv.TUJIAN_TYPE)

        with allure.step(f'识别的验证码为：{img_code}'):
        #将识别的验证码设置问全局变量
            with allure.step(f'设置全局变量imgcode:{img_code}'):
                setattr(SystemEnv,'imgcode',img_code)
        
        logger.info(f'设置全局变量imgcode:{img_code}')
    except:
        logger.error('请判断接口返回的是否是一个二进制文件/图片')