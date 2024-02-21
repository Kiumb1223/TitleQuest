#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
:File       :download.py
:Description:编写爬虫程序实现爬取每篇文章的pdf下载连接
             其中需要在 GoogleScholar文件中的代理函数设置自己的代理
:EditTime   :2024/02/19 19:24:46
:Author     :Kiumb
'''


import os 
import urllib
import GoogleScholar
from lxml import etree
import random
import time
import csv


# 遍历cai_teacher_articles文件夹中的所有文件
agents = GoogleScholar.read_agents(r'config\agents.txt')    # 获取所有UA
# domains = GoogleScholar.read_domains(r'config\domains.txt')    # 获取所有域名
# 统计数据记录
totalNumber_citationpaper = 0                               # 记录总的引用文件数量
statisticsPath = os.path.join('cai_teacher_articles','statisticalData.txt')

for root , dirs , files in os.walk('cai_teacher_articles'):
    for idx_file,file_name in enumerate(files):
        if not file_name.endswith('.txt') or file_name == 'statisticalData.txt':
            continue
        print(f'{idx_file + 1} articles : {file_name}')
        filePath = os.path.join('cai_teacher_articles',file_name)
        # 读取单个文本中的信息，并且保存为excel
        # filePath = 'cai_teacher_articles\A comprehensive and fair comparison of two neural operators (with practical extensions) based on fair data.txt'
        with open(filePath,'r',encoding='utf-8') as file:
            lines = file.readlines()

        # 创建以该文件名命名的文件夹
        output_dir = os.path.join('cai_teacher_articles',os.path.basename(filePath).split('.')[0])
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        elif os.path.exists(os.path.join(output_dir,'pdf_link_result.csv')):
            print("Finished")
            print('-------------------------------------------------------------------------------')
            continue

        article_list = []
        Nofound_num = 0
        for idx_line , line in enumerate(lines): 
            # 遍历每篇文章，爬取它们的pdf下载链接
            citation_file_title = line.strip()
            # print(f'{idx + 1 }:{citation_file_title}')
            # 构造搜索URL
            searchUrl = r'https://scholar.google.com.hk/scholar?hl=zh-CN' + '&q=' + urllib.parse.quote(citation_file_title)

            # 构造代理以及header爬取文件的pdf下载链接
            # with open('./config/config.txt', 'r', encoding='utf-8') as proxy_file:  # 打开文件
            #     lines_config = proxy_file.readlines()  # 读取所有行
            #     proxy = {'https': 'https://' + lines_config[0].replace('\n', ''),'http': 'http://' + lines_config[0].replace('\n', '')}
            #     agent = lines_config[1].replace('\n', '')
            #     cookie = lines_config[2].replace('\n', '')
            #     # print('[config] cookie: {}'.format(cookie))
            #     # print('[config] agent: {}'.format(agent))
            agent = GoogleScholar.random.choice(agents)    # 随机选择一个UA
            # domain = GoogleScholar.random.choice(domains)    # 随机选择一个域名
            proxy = GoogleScholar.select_proxy()
            # 构造header
            headers = {
                'authority': 'scholar.google.com.hk',
                'method': 'GET',
                'scheme': 'https',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cookie': 'GSP=LM=1589629500:S=bdTlYLAgGL7KA7s2; NID=204=lT8K8u-_lBsiD7Nmz6g9wkyeRx_eK_aWmJ_q7eZ77r4LpU4BY2lrrKxJ0YDqxBZXnztoRiQYtBS2szDHIW8w-S3BarOochkJZJ9uXYabKtwLp8Zm1IWs0gVpgwRCHpWzzioFMYKN1V9XR9HIa2LtrnZ9kjQu0_LiDBM_WfMhkhc',
                # 'cookie': cookie,
                'dnt': '1',
                'referer': 'https://scholar.google.com.hk/?hl=zh-CN',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent':agent,
                'x-client-data': 'CJe2yQEIpbbJAQjEtskBCKmdygEI0K/KAQi8sMoBCO21ygEIjrrKAQjtu8oBGLy6ygE=',
                # 'Host':domain
            }

            data = GoogleScholar.get_data(searchUrl, headers, proxy)    # 获取数据

            html = etree.HTML(data)    # 解析成html

            try:
                # 有些文章 在GoogleScholar中未提供下载链接
                # 获取 pdf下载链接
                pdf_link = html.xpath('//*[@id="gs_res_ccl_mid"]/div/div[1]/div/div/a/@href')[0]
            except:
                pdf_link = 'None'
                Nofound_num += 1 
            article_dict = {
                'Title':citation_file_title,
                'PDF Link':pdf_link
            }
            delay_time = random.randint(2,5)    # 延时随机数
            # print('开始延时 {}s，程序没有崩，请耐心等待...'.format(delay_time))
            time.sleep(delay_time)    # 随机延时一段时间，对付狗贼谷歌
            # print('为您延时 ' + str(delay_time) + 's 成功！')    # 随机延迟，防止反爬识别
            # print('-------------------------------------------------------------------------------')

            article_list.append(article_dict)       
        print(f'Total Number of articles : {idx_line + 1} \nMiss Pdf Link : {Nofound_num}')
        print('-------------------------------------------------------------------------------')

        # 写入数据到CSV文件中
        csv_file_path = os.path.join(output_dir,'pdf_link_result.csv')
        fields = ['Title','PDF Link']
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            # 写入列名
            writer.writeheader()
            # 写入数据
            for item in article_list:
                writer.writerow(item)

        # 记录统计数据到statisticalData.txt中
        with open(statisticsPath,'a+',encoding='utf-8') as file:
            file.write(f'{idx_file + 1} articles : {file_name}\n')
            file.write(f'Total Number of articles : {idx_line + 1} \nMiss Pdf Link : {Nofound_num}\n')
            file.write('-------------------------------------------------------------------------------\n')

    totalNumber_citationpaper  += idx_line
    
        # GoogleScholar.sava_to_excel(article_list,os.path.join(output_dir,'result.xlsx'))
    
# 记录总的引用文章总数
with open(statisticsPath,'a+',encoding='utf-8') as file:
    file.write(f'totalNumber_citation_atticle : {totalNumber_citationpaper}\n')