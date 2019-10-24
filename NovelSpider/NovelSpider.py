#!/usr/bin/python
# -*- coding:utf-8 -*-

#总的小说爬取
#version 1.1.0
#latest update 2019/10/16
#已收录网站：
#5200免费全本小说网 https://qxs.la/       latest update:2019/10/16
#醋溜儿文学网 http://www.clewx.com/      latest update:2019/10/20

import urllib.request as urllib2
from GetHtml import GetHtml_2 as GetHtml
from bs4 import BeautifulSoup
import threading
import re
import time

class Producer(threading.Thread):
    def __init__(self, url, start_url, end_url):
        threading.Thread.__init__(self)
        self.url = url
        self.start_url = start_url
        self.end_url = end_url
        
        
    def run(self):
        html = GetHtml(self.url, timeout=3)
        while html == None:
            html = GetHtml(self.url, timeout=4)
        if webPage == "https://qxs.la/":
            chapters = re.findall(r'<div class=\"chapter\">.*?<a href=\"(.*?)\"', html, re.S)
            self.start_url = self.start_url[14:]
            self.end_url = self.end_url[14:]
            start = chapters.index(self.start_url)
            end = chapters.index(self.end_url) + 1
            chapters=chapters[start:end]
            for s in chapters:
                url = "https://qxs.la" + s
                writer.addUrl(url)
                #give the url to the most free one
                minn = 6666
                minid = -1
                for consumer in consumer_list:
                    if consumer.GetRemainedTasks() < minn:
                        minn = consumer.GetRemainedTasks()
                        minid = consumer.GetId()
                consumer_list[minid].addUrl(url)
        elif webPage == "http://www.clewx.com/":
            #没有re.S会单行匹配，有re.S会多行匹配
            chapters = re.findall(r'<dd><a href=\"(.*?)\" title', html)
            print(chapters)
            start = chapters.index(self.start_url)
            end = chapters.index(self.end_url) + 1
            chapters=chapters[start:end]
            for url in chapters:
                writer.addUrl(url)
                #give the url to the most free one
                minn = 6666
                minid = -1
                for consumer in consumer_list:
                    if consumer.GetRemainedTasks() < minn:
                        minn = consumer.GetRemainedTasks()
                        minid = consumer.GetId()
                consumer_list[minid].addUrl(url)
        elif webPage == "http://www.k6uk.com/":
            


class Writer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.url_list = []
        
    def addUrl(self, url):
        self.url_list.append({"state":False, "url":url, "content":""})
        
    def run(self):
        with open(r'C:\Users\MEC\Desktop\xs\000.txt', 'a+', encoding='utf-8') as f:
            while Producer_Flag or self.url_list != []:
                    if self.url_list != [] and self.url_list[0]["state"]:#consumer has downloaded the text
                        f.write(self.url_list[0]["content"])
                        print(" [+] Writer downloaded ", self.url_list[0]["content"][:self.url_list[0]["content"].find("\n")])#print title
                        del(self.url_list[0])
                    
    def write(self, url, title, content):
        for i in range(len(self.url_list)):
            if self.url_list[i]["url"] == url:
                self.url_list[i]["state"] = True
                self.url_list[i]["content"] = title + "\n" + content +"\n"
                break
    
class Consumer(threading.Thread):
    def __init__(self, url_list, id):
        threading.Thread.__init__(self)
        self.url_list = url_list
        self.id = id
        
    def GetRemainedTasks(self):
        return len(self.url_list)
    
    def GetId(self):
        return self.id
    
    def addUrl(self, url):
        self.url_list.append(url)
    
    def run(self):
        while Producer_Flag or self.url_list != []:
            if self.url_list != []:
                html = GetHtml(self.url_list[0])
                while html == None:
                    html = GetHtml(self.url_list[0])
                url = self.url_list[0]
                del(self.url_list[0])
                
                try:
                    bs = BeautifulSoup(html,'html.parser')#standard library
                    title = self.getTitle(bs)
                    content = self.getContent(bs)
                    print(" [+] Spider{0}: {1} parsed".format(self.id, title))
                    writer.write(url, title, content)
                except Exception as e:
                    print(" [-] Spider{0}: {1}\n\twhen parsing {2}".format(self.id, e, url))
                    #parse again
                    self.url_list.insert(0, url)
        
        print(" [-] Spider {0} finished...".format(self.id))
                
    def getTitle(self, bs):
        ts=""
        if webPage == "http://www.clewx.com/":
            #get meta in head
            ts = bs.find(attrs={'name':'description'})["content"]
            ts = ts[27:]
        elif webPage == "http://www.k6uk.com/":
            ts = bs.find('div', {'id':'title'}).text
        elif webPage == "https://qxs.la/":
            ts= bs.find('div', {'class':'text t_c'}).text #get h1
        elif webPage == "http://m.shwx.org/sj.php":
            text = bs.find('div', {'class':'nr_title', 'id':'nr_title'})
            ts = text.text.replace('    	 ', '')
        elif webPage == "https://www.630book.la/":
            text = bs.find('title').text
            ts=text[:-10]#omit后面10个
        return ts.strip()

    def getContent(self, bs):
        t=""
        if webPage == "http://www.clewx.com/":
            ts = bs.find("div",{'class':'content fz14'})
            t = ts.text.replace('　　', '\n 　　')
        elif webPage == "http://www.k6uk.com/" or webPage == "https://qxs.la/" or webPage == "https://www.630book.la/":
            t = bs.find('div', {'id':'content'})
            te = t.text
            te = te.replace('　　', '\n    ')
            t = te.replace('(手机阅读请访问m.k6uk.com)', '')
            t = te.replace('(ｗww.ｋ6uk.ｃom)', '')
            t = te.replace('(www.k6ｕk.com)', '')
            t = te.replace('(wwｗ.k6uｋ.coｍ)', '')
            te = te.replace('全新的短域名 qxs.la 提供更快更稳定的访问，亲爱的读者们，赶紧把我记下来吧：qxs.la （全小说无弹窗）', '')
            te = te.replace('ad1();ad2();ad3();', '')
            te = te.replace('恋上你看书网 WWW.630BOOK.LA ，最快更新痴念最新章节！', '')
            te = te.replace('\n\n', '')
            te = te.replace('【本章节首发．爱．有．声．小说网,请记住网址】', '')
            te = te.replace('22ff。com', '')
            te = te.replace('/', '')
            te = te.replace('www*ttzw*com', '')
            te = te.replace('www@ttzw@com', '')
            t = te.replace('ad4();ad5();ad6();', '')
        elif webPage == "http://m.shwx.org/sj.php":
            texts = bs.find('div', {'id':'nr1'})
            t = texts.text.replace('<br/>', '')
            t = t.replace('请记住我们的地址【www.ShuhUang.NET】', '')
            t = t.replace('www.shuhuang.net为您提供最新最快最全的免费VIP小说', '')
            #取第7个以后的字符，为了去掉空格
            t = t[7:]
        return t.strip()

if __name__=="__main__":
    #下载要求信息
    #######catalog
    catalog_url = "http://www.clewx.com/book/201909/25/10459.html"
    start_url = "http://www.clewx.com/book/201909/25/10459_3610810.html"
    end_url = "http://www.clewx.com/book/201909/25/10459_3613663.html"
    global webPage
    webPage = "http://www.clewx.com/"
    #下载要求信息
    
    global Producer_Flag
    Producer_Flag = True
    
    ###init consumers
    consumer_num = 6
    global consumer_list
    consumer_list = []
    for i in range(consumer_num):
        print(" [+] Spider {0} is running...".format(i))
        consumer = Consumer([], i)
        consumer.start()
        consumer_list.append(consumer)
       
    #init writer
    print(" [+] Writer is running...")
    global writer
    writer = Writer()
    writer.start()
       
    #init producer
    print(" [+] Producer is running...")
    producer = Producer(catalog_url, start_url, end_url)
    producer.start()
    
    producer.join()
    Producer_Flag = False
    print(" [-] Producer finished...")
    for consumer in consumer_list:
        consumer.join()    
    print(" [-] All Spiders finished...")
    writer.join()
    print(" [-] Writer finished...")
    
