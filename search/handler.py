#-*- coding: utf-8 -*-
import os
import json
import re
import shutil
import requests
from elasticsearch import Elasticsearch
from bs4 import BeautifulSoup

class handler:
    website = ''
    urllist = []
    es = ''

    def __init__(self, url_list):
        self.urllist = url_list
        self.es = Elasticsearch()

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
            soup = BeautifulSoup(open(htmlpath), "html5lib")
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
        index, type, id = self.geturl(url)  
        params = json.dumps(payload,ensure_ascii=False) 
        re = self.es.index(index = index, doc_type = type, id = id, body = params)
        print re

    def handleEmpty(self, str):
        if str:
            return str
        else:
            return "none"

    def geturl(self, url):
        codeArr = url.split('/')
        crop = self.handleEmpty(codeArr[0])
        id = self.handleEmpty(codeArr[-1])
        codeArr = codeArr[1:-1]
        type = ''.join(codeArr) 
        type = self.handleEmpty(type)
#        queryurl = "curl -XPUT http://localhost:9200" + '/' + crop + '/' + type + '/' + id + '-d'
        return crop, type, id 
