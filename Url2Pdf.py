#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
:File       :Url2Pdf.py
:Description: 实现根据url下载pdf
              主要是根据目标文件树的关系来遍历下载pdf
              最后会在对应的文件夹里面生成download.log日志文件，保存失败下载的信息
:EditTime   :2024/02/19 20:57:29
:Author     :Kiumb
'''

import os
import time 
import shutil
import random
import pandas as pd 
import PDFDownload


# 定义文件夹路径
folder_path = 'cai_teacher_articles'
log         = 'download.log'    # 记录下载未成功的文章以及PDF链接
# 遍历文件夹
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file == 'pdf_link_result.csv':
            print(f'{root}')
            with open(os.path.join(root,log),'a+',encoding = 'utf-8') as f:
                csv_path = os.path.join(root,file)
                df = pd.read_csv(csv_path,sep='#')
                article_list = df.to_dict(orient='records')
                failed_cnt = 0
                for article in article_list:
                    failedArticle = PDFDownload.get_file(article,root)
                    if failedArticle != {} :
                        failed_cnt += 1
                        f.write(f"{failed_cnt} {failedArticle['Title']}   {failedArticle['PDF Link']}\n")
                        print(f"{failed_cnt} {failedArticle['Title']}   {failedArticle['PDF Link']}\n")
                    
                delay_time = random.randint(2,5)    # 延时随机数
                # print('开始延时 {}s，程序没有崩，请耐心等待...'.format(delay_time))
                time.sleep(delay_time)    # 随机延时一段时间，对付狗贼谷歌
                # print('为您延时 ' + str(delay_time) + 's 成功！')    # 随机延迟，防止反爬识别
                
                f.write('-------------------------------------------------------------------------------\n')
                f.write(f'Total_Number : {len(article_list)}    Failed_cnt : {failed_cnt}\n')

                print(f'Total_Number : {len(article_list)}    Failed_cnt : {failed_cnt}')
                print('-------------------------------------------------------------------------------')