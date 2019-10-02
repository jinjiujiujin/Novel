#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import random
import time
import lxml
from bs4 import BeautifulSoup

#醋溜儿文学网 http://www.clewx.com/ 
#version: 1.0.0
#author: zyyz
#latest update:2019/8/4

def getHtml(url):
     headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection':'keep-alive',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
        }

     timeOut = random.choice(range(80, 155))
     while True:
        try:
            req = requests.get(url=url, headers = headers, timeout = timeOut)
            break
        except Exception as e:
            print(e)
            time.sleep(random.choice(range(3, 8)))
        i+=1
        if i>20:
            print("connection failed.")
            print("the crawler comes to an end.")
            break;

     return req.content


def getTitle(bs):
    #get meta in head
    ts = bs.find(attrs={'name':'description'})["content"]
    ts = ts[27:]
    return ts

def getContent(bs):
    ts = bs.find("div",{'class':'content fz14'})
    t = ts.text.replace('　　', '\n 　　')
    return t

def write2file(title, content):
    f = open(r'C:\Users\MEC\Desktop\xs\clewx.txt', 'a+', encoding='utf-8')
    f.write(title)
    f.write(content)
    f.write('\n')
    print(title)
    f.close()

def getNextChapter(bs):
    t = bs.find('a', string = '下一章')
    return t['href']

if __name__=="__main__":
    url = "http://www.clewx.com/book/201902/23/10008_3555577.htmlb"
    while url !="javascript:alert('没有下一章了');":
        html = getHtml(url)
        bs = BeautifulSoup(html,'html.parser')#standard library
        title = getTitle(bs)
        content = getContent(bs)
        write2file(title, content)
        url = getNextChapter(bs)