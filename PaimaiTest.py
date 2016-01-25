# -*- coding: utf-8 -*-

'产权交易中心列表抓取'

__author__ = 'ojxing'
__time__ = '2015-12-22'

import re
import requests
import sys
import bs4
import mysql.connector
import ConfigParser

import Email as emal
reload(sys)
sys.setdefaultencoding('utf-8')

class PMSpider():
    def __init__(self):
        print('开始抓取数据')
    def getAllPage(self,url):
        links = []
        for each in range(1,9):
            link = re.sub('page=\d+','page=%s'%each,url)
            links.append(link)
        return links
    def getSource(self,url):
        html = requests.get(url)
        return html.content.decode('gbk').encode('utf-8')
    def getEachPage(self,html):
        #soup = BeautifulSoup(html)
        soup1 = bs4.BeautifulStoneSoup(html)
        paimai = soup1.findChildren(bgcolor="#ffffff")
        return paimai
    def getPaiMaiInfo(self,eachList):
        info = {}
        # info['Name'] = eachList.contents[2].contents[0].contents[0].string[:-6]
        # info['Type'] = eachList.contents[3].contents[0].contents[0]
        # info['Date'] = eachList.contents[4].contents[0].contents[0].string[:-6]
        info['Code'] = eachList.contents[0].contents[2].contents[1].contents[0].contents[0].string[2:]
        info['Name'] = eachList.contents[0].contents[3].contents[0].contents[0].contents[0].string[2:]
        info['Type'] = eachList.contents[0].contents[4].contents[0].contents[0].string[2:]
        info['Date'] = eachList.contents[0].contents[5].contents[1].contents[0].string[2:]
        return info
    def Save(self,paimai_info):
        em = emal.Email()
        db = DB()
        name_list = []
        code_not_in_db=[]
        code_in_db = db.queryData()

        for each in paimai_info:
            if (each['Code'],) not in code_in_db:
                code_not_in_db.append(each)
                name_list.append(each['Name'] + ', ')
        if len(code_not_in_db) >0:
            db.insertData(code_not_in_db)
            em.send_email('584765203@qq.com',' 成功更新数据库，补充数据' + str(len(code_not_in_db)) + '条！新增拍卖信息为'+''.join(name_list),'家兴同学')
            print('成功更新数据库，补充数据' + str(len(code_not_in_db)) + '条！新增拍卖信息为'+''.join(name_list))
        else:
            print('暂无更新条目！')

class DB():
    def __init__(self):
        config = ConfigParser.ConfigParser()
        with open('files/PaiMaiCfg','r') as cfgfile:
            config.readfp(cfgfile)
            self.user = config.get('info','user')
            self.password = config.get('info','password')
            self.host = config.get('info','host')
            self.database = config.get('info','database')
        pass
    def queryData(self):
        P_code_list = []
        cnx = mysql.connector.connect(user=self.user,password=self.password,host=self.host,database=self.database)
        cursor = cnx.cursor()
        query = ("SELECT P_code from paimaiinfo")
        cursor.execute(query)
        result = cursor.fetchall()
        for(P_code) in cursor:
            P_code_list.append(P_code)
        cnx.commit()
        cursor.close()
        cnx.close()

        return result
    def insertData(self,paimais):
        data = []
        for each in paimais:
            da = []
            da.append(each['Code'])
            da.append(each['Name'])
            da.append(each['Type'])
            da.append(each['Date'])
            data.append(da)


        cnx = mysql.connector.connect(user=self.user,password=self.password,host=self.host,database=self.database)
        cursor = cnx.cursor()
        query = ("INSERT INTO paimaiinfo (P_code,P_name,P_type,P_date) VALUES (%s,%s,%s,%s)")
        cursor.executemany(query,data)
        cnx.commit()
        cursor.close()
        cnx.close()
class Paimai():
    def __init__(self,code,name,type,date):
        self.P_code = code
        self.P_name = name
        self.P_type = type
        self.P_date = date

def main():
    url = 'http://www.gemas.com.cn/Project/defaultnew.asp'
    paimai_info =[]
    pmspider = PMSpider()
    links = pmspider.getAllPage(url)
    print '正在抓取' + url
    html = pmspider.getSource(url)
    eachList = pmspider.getEachPage(html)
    for each in eachList:
        paimai = pmspider.getPaiMaiInfo(each)
        paimai_info.append(paimai)
    print('抓取成功！正在保存数据到本地文件...')
    pmspider.Save(paimai_info)

# pa = Paimai('code','ppname','pptype','ppdate')
# db = DB()
# data = db.queryData()
# for each in data:
#     print(each[0])

main()

