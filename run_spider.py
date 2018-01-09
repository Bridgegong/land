# -*- coding: utf-8 -*-
# @Time    : 2018/1/9 10:59
# @Author  : Bridge
# @Email   : 13722450120@163.com
# @File    : run_spider.py
# @Software: PyCharm
import spider
s=spider.Spider()
#日期
year=2018
month=1
day=1
delta=s.timeDelta(year,month)
#一个月一个月的抓取
while day<=delta:
    #日期
    date=s.handleDate(year,month,day)
    #页数
    allNum=s.getAllNum(date)
    #链接
    allLinks=s.getAllLinks(allNum,date)
    #信息
    s.saveAllInfo(allLinks,date)
    day+=1
    print date,'KO!'
print date.strftime('%Y-%m'),'KO!'

