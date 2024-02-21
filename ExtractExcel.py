#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
:File       :extractExcel.py
:Description:实现从excel表格当中提取需要内容，并且保存到文本文件当中
             具体来说是讲 分别保存excel表格中每篇蔡老师文章的引用文章到一个文本文件当中，然后以蔡老师文章的名字来命名
:EditTime   :2024/02/21 16:00:38
:Author     :Kiumb
'''

import pandas as pd
import os

# 加载Excel文件
file_path = '文献引用汇总(1).xlsx'
excel_data = pd.ExcelFile(file_path)

# 从工作表中加载数据
sheet_data = pd.read_excel(excel_data, 'Sheet1')

# 创建存储文本文件的目录
output_dir = 'cai_teacher_articles'
os.makedirs(output_dir, exist_ok=True)

# 初始化变量
current_article = None
file_paths = []

def sanitize_filename(filename):
    """
    清理文件名，移除或替换非法字符，并确保文件名长度不超过255字符。
    """
    sanitized = filename.replace(':', '_')
    return sanitized[:255]

for index, row in sheet_data.iterrows():
    # 检查行中是否有新的蔡老师文章
    if pd.notnull(row['蔡老师文章详情']):
        # 如果发现新文章，保存前一篇文章（如果有）
        if current_article:
            sanitized_title = sanitize_filename(current_article)
            file_path = os.path.join(output_dir, f"{sanitized_title}.txt")
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write('\n'.join(referencing_articles))
            file_paths.append(file_path)

        # 开始新的引用文章列表
        current_article = row['蔡老师文章详情']
        referencing_articles = []

    # 将引用文章标题添加到列表中
    if pd.notnull(row['引用者文章']):
        referencing_articles.append(row['引用者文章'])  # 只取第一行（标题）

# 保存最后一篇文章
if current_article:
    sanitized_title = sanitize_filename(current_article)
    file_path = os.path.join(output_dir, f"{sanitized_title}.txt")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(referencing_articles))
    file_paths.append(file_path)
