#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
:File       :GoogleScholar.py
:Description:用于爬取谷歌学术的爬虫的功能性文件
:EditTime   :2024/02/19 19:24:56
:Author     :Kiumb
'''


import urllib.request as request    # 用于请求数据
import requests    # 用于请求数据
from urllib import parse    # 用于encodeURIComponent编码与解码
import random    # 用于随机生成ua
import os    # 用于文件路径相关的操作
import gzip    # 用于解压谷歌学术返回的数据
import io   # 用于字符流操作
from lxml import etree    # 用于xpath解析
import re    # 用于处理正则表达式
import time    # 用来延时，有效防止被封
import urllib.error    # 用来处理url请求错误
import pandas as pd    # 用于将字典列表转换为DataFrame并将其导出到Excel文件
import http.cookiejar as cookielib    # 用于处理cookie
from retrying import retry    # 用于url打开错误重试
import gc    # 用于垃圾回收

# 读取所有agents
def read_agents(filename):
    agents=[]
    agents_file=open(filename,'r',encoding='utf-8')
    for r in agents_file.readlines():
        data="".join(r.split('\n'))
        agents.append(data)
    agents_file.close()
    del agents_file
    del data
    gc.collect()
    return agents

# 读取所有域名
def read_domains(filename):
    domains = []
    domains_file = open(filename,'r',encoding='utf-8')
    for r in domains_file.readlines():
        data="".join(r.split('\n'))
        domains.append(data)
    domains_file.close()
    del domains_file
    del data
    gc.collect()
    return domains

# 读取所有代理ip
def read_ips(filename):
    ips = []
    ips_file = open(filename, 'r', encoding='utf-8')
    for r in ips_file.readlines():
        data="".join(r.split('\n'))
        ips.append(data)
    ips_file.close()
    del ips_file
    del data
    gc.collect()
    return ips

# 自定义代理
def select_proxy(proxy_type='socks-client'):
    proxies = {}
    if proxy_type == 'http':
        # 代理设置：http(s)代理
        proxies = {
            'https': 'https://127.0.0.1:2173',
            'http': 'http://127.0.0.1:2173'
        }
    elif proxy_type == 'socks-remote':
        # 代理设置：socks5代理（远程服务器）
        proxies = {
            'socks5': 'socks5://user:pass@host:port',
            'socks5': 'socks5://user:pass@host:port'
        }
    elif proxy_type == 'socks-client':
        # 代理设置：socks5代理（客户端在本机）
        proxies = {
            'http': 'socks5://127.0.0.1:7890',
            'https': 'socks5://127.0.0.1:7890'
        }
    elif proxy_type == 'no':
        # 代理设置：不使用代理
        proxies = {}
    else:
        pass
    return proxies

# 指定url，获取网页内容
@retry(stop_max_attempt_number=5, wait_random_min=10, wait_random_max=20)    # 请求失败自动重试
def get_data(url, headers, proxies):
    # 使用urllib
    # print('--------------正在使用urllib获取数据--------------')
    # print('获取网页数据...')
    cookie = cookielib.CookieJar()    # 写到最后才发现好多网站需要cookie，索性就在这儿设置了
    request.build_opener()
    opener = request.build_opener(request.ProxyHandler(proxies), urllib.request.HTTPCookieProcessor(cookie))    # 设置代理和cookie处理器
    request.install_opener(opener)    # 安装代理
    req = request.Request(url, headers=headers)    # 设置请求
    # response = request.urlopen(req)    # 打开url
    # 准备使用try，有点小毛病，待改进
    try:
        response = request.urlopen(req)    # 打开url
        content_type = response.info().get('Content-Type', '')  # 获取Content-Type头部

        # print("Connection Succeeded!")
        # print(response.read().decode())    # 输出响应内容，由于返回的是压缩文件，这种方式已经不行了
        # 根据不同的编码格式处理数据
        if response.info().get('Content-Encoding') == 'gzip':
            data = gzip.decompress(response.read()).decode("utf-8")    # 如果是压缩格式则解压
        else:
            # 尝试根据Content-Type头部指定的编码解码，如果没有指定则默认使用utf-8
            charset = 'utf-8'
            if 'charset=' in content_type:
                charset = content_type.split('charset=')[-1]
            data = response.read().decode(charset, errors='ignore')  # 使用指定编码解码，忽略错误
        # print(data)    # 输出处理后的数据
        del cookie
        del opener
        response.close()
        del response
        gc.collect()
        return data
    except urllib.error.URLError as e:
        print('GoogleScholar.get_data()：' + str(e.reason))
    except UnicodeDecodeError as e:
        print('解码错误：', e)
    return

