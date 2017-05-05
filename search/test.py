#-*- coding:utf-8 -*-
import requests
import os
import shutil
from bs4 import BeautifulSoup
import handler

url = 'http://123.xidian.edu.cn/'
r = requests.get(url)
soup = BeautifulSoup(r.text)





handler = handler.handler(['www.xidian.edu.cn'])
handler.handle()
