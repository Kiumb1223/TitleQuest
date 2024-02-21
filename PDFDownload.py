#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
:File       :PDFDownload.py
:Description:用于下载pdf的功能性文件
:EditTime   :2024/02/19 14:43:41
:Author     :Kiumb
'''

import urllib.request    # 用于网络连接，即PDF下载
import os    # 用于文件操作，例如删除、重命名
import pandas as pd    # 用于Excel读取及Dataframe转换
from copy import deepcopy    # 用于字典的深拷贝
from retrying import retry    # 用于下载错误重试
import gc    # 用于解决内存泄漏

def sanitize_filename(filename):
    """
    清理文件名，移除或替换非法字符，并确保文件名长度不超过255字符。
    """
    sanitized = filename.replace(':', ' ')
    return sanitized[:255]


# 下载文件
def get_file(article, path):
    '''
    :Description:
    :Parameter  : article :文章名字以及下载链接
                  path： 保存pdf文件的路径
    :Return     :
    '''
    url = article['PDF Link']
    savePath = os.path.join(path,sanitize_filename(article['Title']) + '.pdf')
    # print('开始下载' + url)
    # print(filename)    # 输出文件名
    # print(url)    # 输出要下载的URL
    error_article = {}

    # 打开链接
    openurl_flag = False
    # 打开链接
    openurl_flag = False
    try:
        data = urllib.request.urlopen(url)
        openurl_flag = True
    except Exception:
        # print('URL打开失败，继续下载下一个。')
        error_article = deepcopy(article)
    finally:
        gc.collect()

    # 下载文件
    if openurl_flag:
        try:
            pdf_file = open(savePath, 'wb')
            block_sz = 8192
            while True:
                buffer = data.read(block_sz)
                if not buffer:
                    break
                pdf_file.write(buffer)
            pdf_file.close()
            data.close()
            del data
            gc.collect()
            # print (savePath)
            # print ("Sucessful to download" + " " + article['Title'])
        except Exception:
            # print('下载出错，继续下载下一个。')
            error_article = deepcopy(article)
    del url
    del openurl_flag
    gc.collect()
    return error_article