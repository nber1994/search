#-*- coding: utf-8 -*-
import os
import re
import shutil
import requests
from bs4 import BeautifulSoup

class handler:
    website = ''
    urllist = []

    def __init__(self, url_list):
        self.urllist = url_list

    def handle(self):
        #将对应文档建立索引        
        for url in self.urllist:
            data = self.pickData(url) 
            self.createIndex(url, data)     

    def pickData(self, url):
        #读取文档
        htmlpath = os.path.abspath('.') + '/' + url 
        data = dict()
        if os.path.exists(htmlpath):
            soup = BeautifulSoup(open(htmlpath), "lxml")
            title = soup.title.string
            [script.extract() for script in soup.findAll('script')]
            [style.extract() for style in soup.findAll('style')]
            body = soup.body.getText()
            body = body.replace(' ', '')
            body = body.replace("\n", '')
            data['title'] = title
            data['body'] = body
            data['url'] = url
        return data
            
    def createIndex(self, url, payload):
        queryurl = self.geturl(url)  
        requests.put(queryurl, params = payload)


    def geturl(self, url):
        codeArr = url.split('/')
        crop = codeArr[0]
        id = codeArr[-1]
        codeArr = codeArr[1:-1]
        type = ''.join(codeArr) 
        return queryurl = 'http://localhost:9200' + '/' + crop + '/' + type + '/' + id
