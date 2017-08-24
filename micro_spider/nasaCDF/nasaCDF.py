# -*- coding:utf-8 -*-

import os
import time
import urllib
import urllib2
import re

class nasaCDF:

    #页面初始化
    def __init__(self):
        self.cdfURL =  'https://cdaweb.sci.gsfc.nasa.gov/pub/software/cdawlib/0MASTERS/'

    #获取页面内容
    def getPage(self):
        url = self.cdfURL
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().decode('utf-8')

    #解析页面信息，文件名，创建日期，大小
    def getContents(self):
        page = self.getPage()
        pattern = re.compile(
            '<tr><td.*?"top"><img src="/icons/unknown.gif" alt="\[   ]"></td><td><a href="(.*?)".*?</a></td><td.*?right">(.*?)\s*</td><td.*?right">\s*(.*?)</td>',
            re.S)
        items = re.findall(pattern,page)
        contents = []
        for item in items:
            isac_wi = re.search('^ac_|^wi_',item[0])
            if isac_wi:
                contents.append([item[0],item[1],item[2]])
        return contents

    # 获取文件夹名称
    def getFile(self,filename):
        # 判断cdf文件类型：ac wi
        if filename.find('ac_') > -1:
            file = u'ac'
            pathName = 'ac' + '/' + filename
        elif filename.find('wi_') > -1:
            file = u'wi'
            pathName = 'wi' + '/' + filename
        return file,pathName

    # 保存cdf文件
    def saveCDF(self,cdf,pathName):
        url = urllib.urlopen(self.cdfURL+cdf)
        data = url.read()
        f = open(pathName,'wb')
        f.write(data)
        print u'正在保存一个cdf文件：',pathName
        f.close()

    #创建新目录
    def mkdir(self,path):
        # 判断路径是否存在
        # 存在    True
        # 不存在  False
        isExist = os.path.exists(path)
        if not isExist:
            # 如果不存在则创建目录
            print u'正在创建',path,u'文件夹'
            os.makedirs(path)
            return True
        else:
            # 如果存在则不创建目录
            print u'文件夹',path,u'已成功创建'
            return False

    #保存cdf文件信息
    def saveCDFInfo(self):
        contents = self.getContents()
        for item in contents:
            # item[0]Name,item[1]Last modified,item[2]Size
            print u'发现一个cdf文件:Name ',item[0],u'Last modified ',item[1],u'Size ',item[2]
            cdf = item[0]
            name = item[0]
            # 获取文件夹名称，文件存储路径
            file = self.getFile(name)
            # 文件夹名称
            filename = file[0]
            # 文件存储路径
            path = file[1]
            # 创建文件夹
            self.mkdir(filename)
            # 保存cdf文件
            self.saveCDF(cdf,path)
cdf = nasaCDF()
cdf.saveCDFInfo()