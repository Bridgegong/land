# -*- coding: utf-8 -*-
# @Time    : 2018/1/9 10:55
# @Author  : Bridge
# @Email   : 13722450120@163.com
# @File    : spider.py
# @Software: PyCharm

# -*- coding: gb18030 -*-
'landchina 爬起来！'
import requests
import csv
from bs4 import BeautifulSoup
import datetime
import re
import os


class Spider():
    def __init__(self):
        self.url = 'http://www.landchina.com/default.aspx?tabid=263'
        # 这是用post要提交的数据
        self.postData = {'TAB_QueryConditionItem': '9f2c3acd-0256-4da2-a659-6949c4671a2a',
                         'TAB_QuerySortItemList': '282:False',
                         # 日期
                         'TAB_QuerySubmitConditionData': '9f2c3acd-0256-4da2-a659-6949c4671a2a:',
                         'TAB_QuerySubmitOrderData': '282:False',
                         # 第几页
                         'TAB_QuerySubmitPagerData': ''}
        self.rowName = [u'行政区', u'电子监管号', u'项目名称', u'项目位置', u'面积(公顷)', u'土地来源', u'土地用途', u'供地方式', u'土地使用年限', u'行业分类',
                        u'土地级别', u'成交价格(万元)', u'土地使用权人', u'约定容积率下限', u'约定容积率上限', u'约定交地时间', u'约定开工时间', u'约定竣工时间',
                        u'实际开工时间', u'实际竣工时间', u'批准单位', u'合同签订日期']
        # 这是要抓取的数据，我把除了分期约定那四项以外的都抓取了
        self.info = [
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c2_ctrl',  # 0
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c4_ctrl',  # 1
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r17_c2_ctrl',  # 2
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r16_c2_ctrl',  # 3
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c2_ctrl',  # 4
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c4_ctrl',  # 5
            # 这条信息是土地来源，抓取下来的是数字，它要经过换算得到土地来源，不重要，我就没弄了
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c2_ctrl',  # 6
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c4_ctrl',  # 7
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r19_c2_ctrl',  # 8
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r19_c4_ctrl',  # 9
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c2_ctrl',  # 10
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c4_ctrl',  # 11
            ##                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3_r2_c1_0_ctrl',
            ##                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3_r2_c2_0_ctrl',
            ##                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3_r2_c3_0_ctrl',
            ##                'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3_r2_c4_0_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r9_c2_ctrl',  # 12
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f2_r1_c2_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f2_r1_c4_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r21_c4_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r22_c2',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r22_c4_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r10_c2_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r10_c4_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c2_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c4_ctrl']

    # 第一步
    def handleDate(self, year, month, day):
        # 返回日期数据
        'return date format %Y-%m-%d'
        date = datetime.date(year, month, day)
        #        print date.datetime.datetime.strftime('%Y-%m-%d')
        return date  # 日期对象

    def timeDelta(self, year, month):
        # 计算一个月有多少天
        date = datetime.date(year, month, 1)
        try:
            date2 = datetime.date(date.year, date.month + 1, date.day)
        except:
            date2 = datetime.date(date.year + 1, 1, date.day)
        dateDelta = (date2 - date).days
        return dateDelta

    def getPageContent(self, pageNum, date):
        # 指定日期和页数，打开对应网页，获取内容
        postData = self.postData.copy()
        # 设置搜索日期
        queryDate = date.strftime('%Y-%m-%d') + '~' + date.strftime('%Y-%m-%d')
        postData['TAB_QuerySubmitConditionData'] += queryDate
        # 设置页数
        postData['TAB_QuerySubmitPagerData'] = str(pageNum)
        # 请求网页
        r = requests.post(self.url, data=postData, timeout=30)
        r.encoding = 'gb18030'
        pageContent = r.text
        #        f=open('content.html','w')
        #        f.write(content.encode('gb18030'))
        #        f.close()
        return pageContent

    # 第二步
    def getAllNum(self, date):
        # 1无内容  2只有1页  3 1—200页  4 200页以上
        firstContent = self.getPageContent(1, date)
        if u'没有检索到相关数据' in firstContent:
            print date, 'have', '0 page'
            return 0
        pattern = re.compile(u'<td.*?class="pager".*?>共(.*?)页.*?</td>')
        result = re.search(pattern, firstContent)
        if result == None:
            print date, 'have', '1 page'
            return 1
        if int(result.group(1)) <= 200:
            print date, 'have', int(result.group(1)), 'page'
            return int(result.group(1))
        else:
            print date, 'have', '200 page'
            return 200
            # 第三步

    def getLinks(self, pageNum, date):
        'get all links'
        pageContent = self.getPageContent(pageNum, date)
        links = []
        pattern = re.compile(u'<a.*?href="default.aspx.*?tabid=386(.*?)".*?>', re.S)
        results = re.findall(pattern, pageContent)
        for result in results:
            links.append('http://www.landchina.com/default.aspx?tabid=386' + result)
        return links

    def getAllLinks(self, allNum, date):
        pageNum = 1
        allLinks = []
        while pageNum <= allNum:
            links = self.getLinks(pageNum, date)
            allLinks += links
            print 'scrapy link from page', pageNum, '/', allNum
            pageNum += 1
        print date, 'have', len(allLinks), 'link'
        return allLinks

    # 第四步
    def getLinkContent(self, link):
        'open the link to get the linkContent'
        r = requests.get(link, timeout=30)
        r.encoding = 'gb18030'
        linkContent = r.text
        #        f=open('linkContent.html','w')
        #        f.write(linkContent.encode('gb18030'))
        #        f.close()
        return linkContent

    def getInfo(self, linkContent):
        "get every item's info"
        data = []
        soup = BeautifulSoup(linkContent)
        for item in self.info:
            if soup.find(id=item) == None:
                s = ''
            else:
                s = soup.find(id=item).string
                if s == None:
                    s = ''
            data.append(unicode(s.strip()))
        return data

    def saveInfo(self, data, date):
        fileName = 'landchina/' + datetime.datetime.strftime(date, '%Y') + '/' + datetime.datetime.strftime(date,
                                                                                                            '%m') + '/' + datetime.datetime.strftime(
            date, '%d') + '.csv'
        if os.path.exists(fileName):
            mode = 'ab'
        else:
            mode = 'wb'
        csvfile = file(fileName, mode)
        writer = csv.writer(csvfile)
        if mode == 'wb':
            writer.writerow([name.encode('gb18030') for name in self.rowName])
        writer.writerow([d.encode('gb18030') for d in data])
        csvfile.close()

    def mkdir(self, date):
        # 创建目录
        path = 'landchina/' + datetime.datetime.strftime(date, '%Y') + '/' + datetime.datetime.strftime(date, '%m')
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)

    def saveAllInfo(self, allLinks, date):
        for (i, link) in enumerate(allLinks):
            linkContent = data = None
            linkContent = self.getLinkContent(link)
            data = self.getInfo(linkContent)
            self.mkdir(date)
            self.saveInfo(data, date)
            print 'save info from link', i + 1, '/', len(allLinks)