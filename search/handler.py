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
    es = ''

    def __init__(self):
        self.es = Elasticsearch(['http://39.108.78.17:9200'])

    def patchIndex(self, indexList):
        #将对应文档建立索引        
        for index in indexList:
            self.setIndex(index)

    def handle(self, urllist):
        for url in urllist:
            try:
                data = self.pickData(url) 
                if data:
                    self.createIndex(url, data)     
            except:
                continue

    def setIndex(self, index):
        if not self.es.indices.exists(index):
            params = {
                    "mappings" : {
                        "_default_" : {
                            "properties" : {
                                "url" : {
                                    "type" : "string",
                                    "index" : "analyzed",
                                    "fields" : {
                                        "cn" : {
                                            "type" : "string",
                                            "analyzer" : "ik_max_word"
                                            },
                                        "py" : {
                                            "type" : "string",
                                            "analyzer" : "pinyin"
                                            },
                                        "en" : {
                                            "type" : "string",
                                            "analyzer" : "english"
                                            }
                                        }
                                    },
                                "title" : {
                                    "type" : "string",
                                    "index" : "analyzed",
                                    "fields" : {
                                        "cn" : {
                                            "type" : "string",
                                            "analyzer" : "ik_max_word"
                                            },
                                        "py" : {
                                            "type" : "string",
                                            "analyzer" : "pinyin"
                                            },
                                        "en" : {
                                            "type" : "string",
                                            "analyzer" : "english"
                                            }
                                        }
                                    },
                                "body" : {
                                    "type" : "string",
                                    "index" : "analyzed",
                                    "fields" : {
                                        "cn" : {
                                            "type" : "string",
                                            "analyzer" : "ik_max_word"
                                            },
                                        "py" : {
                                            "type" : "string",
                                            "analyzer" : "pinyin"
                                            },
                                        "en" : {
                                            "type" : "string",
                                            "analyzer" : "english"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
            self.es.indices.create(index=index, body=params)

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
            if not title:
                return False
            data['title'] = title
            data['body'] = body
            data['url'] = url
            return data
        return False

    def createIndex(self, url, payload):
        index, type, id = self.geturl(url)  
        params = json.dumps(payload,ensure_ascii=False) 
        re = self.es.index(index = index, doc_type = type, id = id, body = params)
        print re
    def isEmpty(self, str):
        if str:
            return str
        else:
            return "-"
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
