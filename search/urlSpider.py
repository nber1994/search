# -*- coding: utf-8 -*  
import os  
import re  
import shutil  
import handler
  
REJECT_FILETYPE = 'rar,7z,css,js,jpg,jpeg,gif,bmp,png,swf,exe,doc,ipa'#定义爬虫过程中不下载的文件类型  
URL_LIST = ['www.xidian.edu.cn']
  

def spider(urlList):
    for url in urlList:
        new_list = getinfo(url)
        handler = handler.handler(new_list)
        handler.handle()


def getOldList(webaddress):
    oldlistpath = os.path.abspath('.') + '/result/' + webaddress + '_result.txt' 
    old_fobj = open(oldlistpath, 'r')
    lines = old_fobj.readlines()
    url_list = []
    for line in lines:
        url_list.append(line[:-1])
    return url_list

def getinfo(webaddress):  
    global REJECT_FILETYPE  
  
    url = 'http://'+webaddress+'/'
    print 'Getting>>>>> '+url

    websitefilepath = os.path.abspath('.')+'/'+webaddress#通过函数os.path.abspath得到当前程序所在的绝对路径，然后搭配用户所输入的网址得到用于存储下载网页的文件夹  
    if os.path.exists(websitefilepath):             #如果此文件夹已经存在就将其删除，原因是如果它存在，那么爬虫将不成功  
        shutil.rmtree(websitefilepath)

    outputfilepath = os.path.abspath('.')+'/'+webaddress+'.txt'    #在当前文件夹下创建一个过渡性质的文件output.txt  
    fobj = open(outputfilepath,'w+')  
    command = 'wget -r -m -nv --reject='+REJECT_FILETYPE+' -o '+outputfilepath+' '+url#利用wget命令爬取网站  
    tmp0 = os.popen(command).readlines()#函数os.popen执行命令并且将运行结果存储在变量tmp0中  
    print >> fobj,tmp0#写入output.txt中  
    allinfo = fobj.read()  
    target_url = re.compile(r'\".*?\"',re.DOTALL).findall(allinfo)#通过正则表达式筛选出得到的网址  
    target_num = len(target_url)  
    fobj1 = open('result/'+webaddress + '_result.txt','w')#在本目录下创建一个result.txt文件，里面存储最终得到的内容  

    new_list = []
    for i in range(target_num):  
        new_list.append(target_url[i][1:-1])
    old_list = getOldList(webaddress)
    new_list = list(set(new_list).difference(set(old_list)))

    for i in range(target_num):  
        print >> fobj1,target_url[i][1:-1]  
    fobj.close()  
    fobj1.close()  
    if os.path.exists(outputfilepath):#将过渡文件output.txt删除  
        os.remove(outputfilepath)#os.remove用于删除文件  
   return new_list 
  
if __name__=="__main__":  
    spider(URL_LIST)
    print "Well Done."#代码执行完毕之后打印此提示信息
