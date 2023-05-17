'''
Author: TylerQA 990687322@qq.com
Date: 2023-04-18 11:28:53
LastEditors: TylerQA 990687322@qq.com
LastEditTime: 2023-05-10 23:21:07
FilePath: \atfx_api\tools\handle_aes.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

"""
项目加密方法
"""

from Crypto.Cipher import AES
import base64
from global_SystemEnv import SystemEnv
from loguru import logger
import allure

"""
出入金加密解密：AES加密
"""
#加密
@allure.step('对字符串进行AES加密')
def encryptData(key:str, iv:str, plaintext:str)->str:
    """
    :param key:加密密匙
    :param iv:加密偏移量
    :param plaintext:需要加密的字符串
    """
    # 将key和iv转换为字节
    key = bytes(key, encoding='utf-8')
    iv = bytes(iv, encoding='utf-8')
    # 使用AES算法进行加密
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 对明文进行PKCS7填充
    plaintext = plaintext.replace(' ','').replace('\t','').replace('\n','').encode('utf-8') #去除所有空字符,换行符。缩进
    padding_length = 16 - len(plaintext) % 16
    padding = bytes([padding_length] * padding_length)
    padded_plaintext = plaintext + padding
    # 使用AES算法加密填充后的明文
    encrypted = cipher.encrypt(padded_plaintext)
    encryp_res = base64.b64encode(encrypted).decode('utf-8')
    # 将加密后的数据进行base64编码
    with allure.step(f'AES加密后的值为：{encryp_res}'):
        logger.info(f'AES加密后的值为：{encryp_res}')
    return encryp_res

#解密
@allure.step('对字符串进行AES解密')
def decryptData(key:str, iv:str, ciphertext:str)->str:
    """
    :param key:加密密匙
    :param iv:加密偏移量
    :param ciphertext:加密后的字符串
    """
    # 将key和iv转换为字节
    key = bytes(key, encoding='utf-8')
    iv = bytes(iv, encoding='utf-8')
    # 对密文进行base64解码
    ciphertext = base64.b64decode(ciphertext)
    # 使用AES算法进行解密
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)
    # 去除解密后数据的PKCS7填充
    padding_length = decrypted[-1]
    decrypted = decrypted[:-padding_length]
    # 将解密后的数据转换为字符串
    decrypt_res = decrypted.decode('utf-8')
    with allure.step(f'AES解密后的值为：{decrypt_res}'):
        logger.info(f'AES解密后的值为：{decrypt_res}')
    return decrypt_res

if __name__ == '__main__':


    key = SystemEnv.VUE_APP_API_ENCRYPT_KEY
    iv = SystemEnv.VUE_APP_API_ENCRYPT_IV
    test_data ={"data":"nl/C0Ud5oHR+5fW39RmGSjtko4+ktVfMqNzn19WFlz2y9GtwPt5PtMOiZlEom4iDlxlKZ6by2qHLW77GHquFWePDpGKeL4Tw9Gkd37b0kwh+8jN0aMfxJcTT4+h5dYtBXc2bdqLfNwyZ7ytywagho74aVq+vCDNP1vV9a6NVXkPvScSQqRwOFx44x9v+XuRQG79yeWr4CV3wJ4gPXosmDqvd1mokjKM67vBVrV7fMHiy+TCDb8PcnzTfPcp1ffu9EB3buO42uqlTop+PFVQexsRS84DtSHfY1rCY6QOUsHD4U1uVuO7va5P4H0EtM+D8FnICAlUTp3NTl8L/fbM5tqqp5w4OFVBcvWXvYVwBmD7n+xGtPvAeLC9j+e2HIAgSL13rjIkEWafaoYkzIFt2NnZFdpmnvvyx5R/y/49eTw2UoQGYpuV4X6B1BSOmsStKzYXTTKUG/FJd7+VhOGDLsBer74dfyDz43VYdqY1pCRaBvi6iwISJw6s3eNk7TOBAeojqfZ4nbQ+ID43ziuUzDfXt0/BZxhUZoI63/vfBXsXrVHbYTqMpfd791uL4CBRfa1H+ph3wEQyG8+3MUjO4yBI3+MmPMev/r9V+143lUsEpJC/o5Nzj9MjUpd6Ly3O6+bGF+sZ6R/Z4+tXVHMcnZPjJLegY4mBT4BmzhaozCAC8ItZElSKztxXMnElA9cbs1AwXk8aJWOHk9l7X/g1uehnE2rM2IDNEyuBQ0N2F73yDb2AjRft6WK1AdJOtuQMEAdGwtJKA8K7B+SM7X+yIn35Ryzzc4ANlN/rqgkJczK7h8HJhFJ40rxlwNKUFemDE9GO9+EFZYOfwkwVM7I0xEzzR+UXM9m7XORTmJ8zk+xXrhPd65EhzKYhu/dXhmHfan3LPEnTx47Sj/jhEgoV1Bjoim0kM9zJ1h/88XCwRHA2DXSf5bngsMR3phWU0GRneoD+fwtzU9ua1EDJfWUsBC/q3BgpZH8EdyvlRcU6WtkPxA3IaO+bJAH5JnbQe9k30"}
    #解密
    res = decryptData(key,iv,test_data.get('data'))

    # test_data2 = """644b909e3cf60000118dda79"""

    # encryptData(key,iv,test_data2)
