#!/usr/bin/python
# -*- coding:utf-8 -*-

#总的小说爬取
#已收录网站：
#醋溜儿文学网 http://www.clewx.com/       latest update:2019/9/15
#看啦又看小说网 http://www.k6uk.com/      latest update:2019/9/15
#书皇小说网 http://m.shwx.org/sj.php      latest update:2019/9/15
#5200免费全本小说网 https://qxs.la/       latest update:2019/9/14
#恋上你看书网 https://www.630book.la/     latest update:2019/9/15

import urllib.request as urllib2
from bs4 import BeautifulSoup

def getTitle(bs, webPage):
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
    return ts

def getContent(bs, webPage):
    t=""
    if webPage == "http://www.clewx.com/":
        ts = bs.find("div",{'class':'content fz14'})
        t = ts.text.replace('　　', '\n 　　')
    elif webPage == "http://www.k6uk.com/" or webPage == "https://qxs.la/" or webPage == "https://www.630book.la/":
        t = bs.find('div', {'id':'content'})
        te = t.text
        te = te.replace('    ', '\n    ')
        t = te.replace('(手机阅读请访问m.k6uk.com)', '')
        t = te.replace('(ｗww.ｋ6uk.ｃom)', '')
        t = te.replace('(www.k6ｕk.com)', '')
        t = te.replace('(wwｗ.k6uｋ.coｍ)', '')
        te = te.replace('全新的短域名 qxs.la 提供更快更稳定的访问，亲爱的读者们，赶紧把我记下来吧：qxs.la （全小说无弹窗）', '')
        te = te.replace('ad1();ad2();ad3();', '')
        te = te.replace('恋上你看书网 WWW.630BOOK.LA ，最快更新痴念最新章节！', '')
        te = te.replace('\n\n', '')
        te = te.replace('/', '')
        t = te.replace('ad4();ad5();ad6();', '')
    elif webPage == "http://m.shwx.org/sj.php":
        texts = bs.find('div', {'id':'nr1'})
        t = texts.text.replace('<br/>', '')
        t = t.replace('请记住我们的地址【www.ShuhUang.NET】', '')
        t = t.replace('www.shuhuang.net为您提供最新最快最全的免费VIP小说', '')
        #取第7个以后的字符，为了去掉空格
        t = t[7:]
    return t

def write2file(title, content):
    f = open(r'C:\Users\MEC\Desktop\xs\000.txt', 'a+', encoding='utf-8')
    f.write(title)
    f.write(content)
    f.write('\n')
    print(title)
    f.close()

def getNextChapter(bs, url, webPage):
    result=""
    if webPage == "http://www.clewx.com/":
        #<a href="http://www.clewx.com/book/201702/24/4317_1098710.html" id="next">下一章</a>
        t = bs.find('a', string = '下一章')
        result=t['href']
    elif webPage == "http://www.k6uk.com/":#有待测试
        ts = bs.find('a', string = '下一页')
        #要求http://www.k6uk.com/novel/62/62464/+1212.html
        i=url.find('/')
        while i!= -1:
            result = url[0:i+1]
            url = url[i+1:]
            i=url.find('/')
        result += ts['href'][2:]#omit开头的./
    elif webPage == "https://qxs.la/":
        ts = bs.find('a', id = "nextLink")
        result = webPage + ts['href']
    elif webPage == "http://m.shwx.org/sj.php":
        text = bs.find('a', id='pb_next')
        result =  'http://m.shwx.org'+text['href']
    elif webPage == "https://www.630book.la/":
        text= bs.find('a', {'class':'nextpage'})
        result = "https://www.630book.la"+text['href']
    return result

def GetHtml(url, encode = "utf-8"):
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection':'keep-alive',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
       }
    request = urllib2.Request(url, headers = headers)
    response = urllib2.urlopen(request)#这是一个 对象
    html = response.read()#无法显示中文
    html = html.decode(encode)
    #会出现该错误
    #'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte
    #但将headers中的   'Accept-Encoding':'gzip, deflate'删掉错误就会消失
    #原理：若有上句，则服务器传过来压缩过的数据，需要额外的deflate算法来解压。
    return html

if __name__=="__main__":
    #下载要求信息
    url = "https://www.630book.la/shu/96778/29146853.html"
    webPage = "https://www.630book.la/"
    encode = "gbk"
    endUrl="https://www.630book.la/shu/96778.html"
    #下载要求信息

    while url != endUrl:
        html = GetHtml(url, encode)
        bs = BeautifulSoup(html,'html.parser')#standard library
        title = getTitle(bs, webPage)
        content = getContent(bs, webPage)
        write2file(title, content)
        url = getNextChapter(bs, url, webPage)
        
