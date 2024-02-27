#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
:File       :excel2pdf.py
:Description:  1. 根据老师提供的xlsx，提取引用者文章中一列的所有有内容的单元格保存到文本文件中
               2. 构造URL保存到csv文件中
               3. 根据csv文件爬取pdf文件
:EditTime   :2024/02/27 10:15:26
:Author     :Kiumb
'''

import os 
import csv
from tqdm import tqdm
import time
import urllib
import random
import pandas as pd 
import GoogleScholar
import PDFDownload
from lxml import etree

excel_path  = '找.xlsx'
article_name_txt = 'article_name.txt'
article_url_csv  = 'article_url.csv'
article_pdf_log  = 'article_pdf_download.log'  # 记录pdf下载结束之后的日志信息 

output_dir  = 'cai_teacher_articles'
article_name_dir  = os.path.join(output_dir,'article_log')  
article_name_path = os.path.join(article_name_dir,article_name_txt)

article_url_dir   = os.path.join(output_dir,'article_log')  
article_url_path  = os.path.join(article_url_dir,article_url_csv)

article_pdf_dir   = os.path.join(output_dir,'article_log')
article_pdf_path  = os.path.join(article_pdf_dir,article_pdf_log)

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

if not os.path.exists(article_name_dir):
    os.mkdir(article_name_dir)

if not os.path.exists(article_url_dir):
    os.mkdir(article_url_dir)

#---------------------------------#
#  1. 读取xlsx文件，保存引用者文章的文本文件
#  保存格式为  单元格行序号#单元格内容
#  注：单元格行序号为后续pdf下载时，文件命名的方式  
#---------------------------------#
if not os.path.exists(article_name_path):   
    excel_data = pd.ExcelFile(excel_path)
    sheet_data = pd.read_excel(excel_data,'Sheet1')
    with open(article_name_path,'a+',encoding='utf-8') as file: 
        for index , row in sheet_data.iterrows():
            if pd.notnull(row['引用者文章']):
                file.write(f"{index+2}#{row['引用者文章']}\n")

print(f'1  Successfully generate {article_name_path}')


#---------------------------------#
#  2. 读取引用者文章的文本文件，构造GoogleScholar访问的URL，
#    爬取pdf下载连接，并保存到csv文件中 
#---------------------------------#

agents = GoogleScholar.read_agents(r'config\agents.txt')    # 获取所有UA

with open(article_name_path,'r',encoding='utf-8') as f:
    article_list_temp = f.readlines()

article_name_list = [item.strip().split('#') for item in article_list_temp]
#  [ ['1','article'] ... ]

article_url_list = []
for item in tqdm(article_name_list):
    # print(item)
    article_index = item[0]
    article_name  = item[1]
    # for index , name in item:
    searchUrl = r'https://scholar.google.com.hk/scholar?hl=zh-CN' + '&q=' + urllib.parse.quote(article_name)
    agent = GoogleScholar.random.choice(agents)    # 随机选择一个UA
    proxy = GoogleScholar.select_proxy()
    # 构造header
    headers = {
        'authority': 'scholar.google.cz',
        'method': 'GET',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        # 'cookie': 'GSP=LM=1589629500:S=bdTlYLAgGL7KA7s2; NID=204=lT8K8u-_lBsiD7Nmz6g9wkyeRx_eK_aWmJ_q7eZ77r4LpU4BY2lrrKxJ0YDqxBZXnztoRiQYtBS2szDHIW8w-S3BarOochkJZJ9uXYabKtwLp8Zm1IWs0gVpgwRCHpWzzioFMYKN1V9XR9HIa2LtrnZ9kjQu0_LiDBM_WfMhkhc',
        # 'cookie': cookie,
        'cookie': 'GSP=LM=1706922270:S=iidEN56Q71NsUs2c; __Secure-3PSID=g.a000gAghe_3HGNqMHSs3ueo-xjQ2s8d8MFs8BIWmmxQE6uR7ohvPBbv-mcqYxHesa8URv_8-jwACgYKAdESAQASFQHGX2MiKRIWo56ifqL4lBzXfM_OixoVAUF8yKrxB4bzeE27K1KiEupUE3i60076; __Secure-3PAPISID=KsOua7I2vQpfDW8W/AcK5F2H2qEnejq3su; 1P_JAR=2024-02-07-06; __Secure-3PSIDTS=sidts-CjEBYfD7Z4sjTaTnOugus22-qGwtZQbZFKv0XBWd_TeameGVfIbhYl0h-Op6v4rJyz6FEAA; __Secure-3PSIDCC=ABTWhQEFNWpiNacURHmfv_apvqdRrEzOhE3jCBPxlEDA1V7IdVtv1m9hXKrs3T5qXqLtO6bC',
        'dnt': '1',
        'referer': 'https://scholar.google.cz/schhp?hl=zh-CN',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        # 'user-agent':agent,
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        # 'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        'x-client-data': 'CJe2yQEIpbbJAQjEtskBCKmdygEI0K/KAQi8sMoBCO21ygEIjrrKAQjtu8oBGLy6ygE=',
        # 'Host':domain
    }

    data = GoogleScholar.get_data(searchUrl, headers, proxy)    # 获取数据

    try:
        html = etree.HTML(data)    # 解析成html
        # 有些文章 在GoogleScholar中未提供下载链接
        # 获取 pdf下载链接
        pdf_link = html.xpath('//*[@id="gs_res_ccl_mid"]/div/div[1]/div/div/a/@href')[0]
    except:
        pdf_link = 'None'
    
    article_dict = {
        'Index':article_index,
        'Title':article_name,
        'PDF Link':pdf_link
    }
    delay_time = random.randint(2,5)    # 延时随机数
    time.sleep(delay_time)    # 随机延时一段时间，对付狗贼谷歌

    article_url_list.append(article_dict)    

# 写入数据到csv文件中
fields = ['Index','Title','PDF Link']
with open(article_url_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fields,delimiter='#')
    # 写入列名
    writer.writeheader()
    # 写入数据
    for item in article_url_list:
        writer.writerow(item)
   
print(f'2  Successfully generate {article_url_path}')

#---------------------------------#
#  3. 读取pdf下载链接文件，下载pdf文件
#---------------------------------#

with open(article_pdf_path,'a+',encoding='utf-8') as f:
    df = pd.read_csv(article_url_path,sep='#')
    article_url_list = df.to_dict(orient='records')
    for article_url in tqdm(article_url_list):
        failArticle = PDFDownload.get_file(article_url,output_dir,default='Index')
        if failArticle!={}:
            f.write(f"{failArticle['Index']}#{failArticle['Title']}#{failArticle['PDF Link']}\n")
        
        delay_time = random.randint(2,5)    # 延时随机数
        time.sleep(delay_time)    # 随机延时一段时间，对付狗贼谷歌

