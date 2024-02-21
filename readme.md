# TitleQuest

> 汇总在帮助我可爱的小硕导申请帽子过程中编写的脚本

## Introduction

在完成筛选所有引用者文章之后，我们需要查看具体大牛们对小硕导文章的评价。这就需要我们把这么多引用者文章下载下来，并具体查看文章中的评价。

本项目实现就是**从GoogleScholar中爬取文章的下载连接，然后下载这些文章**。

具体而言，我需要根据`文献引用汇总(1).xlsx`中的23篇硕导的文章，下载将其引用的347篇文章的pdf。

实现思路其实非常简单：

1. **ExtractExcel.py**:首先将347篇文章按照`文献引用汇总(1).xlsx`分成23类，并且分别保存到相对应的以硕导的文章名命名的文本文件中;
2. **ExtractPdfLink.py**:读取这23个文本文件，根据里面的文章名字，构造GoogleScholar搜索的url，然后爬取搜索结果页面，使用xpath格式来匹配pdf下载链接。并且创建了对应的23个文件夹，在各个文件夹下保存对应的`pdf_link_result.csv`;
3. **Url2Pdf.py**:读取23个文件夹下的csv文件，进行pdf文件的下载,并且会生成日志信息，保存未能成功下的文章信息。

## Limitations Summary

1. **ExtractPdfLink.py**
   * 部分文章在GoogleScholar中不存在pdf下载链接，所以返回None；
   * xpath格式匹配不在精确，部分文章不能正确匹配下载链接。
2. **Url2Pdf.py**
   * pdf下载的爬虫只是简单伪装，所以不能绕过比如**ScienceDirect**等网站的人机验证，因此就不能下载。最后的347篇文章，只能爬下来124篇；
   * 其次，在保存pdf文件的过程中，是以原本文章的名字来命名，但是部分文章名存在特殊字符或者长度等问题导致在windows下的非法文件名，从而导致不能成功保存。

## Reference

1. [GitHub - Dao-zhi/GoogleScholarGUI: 谷歌学术爬取GUI版本](https://github.com/Dao-zhi/GoogleScholarGUI)

