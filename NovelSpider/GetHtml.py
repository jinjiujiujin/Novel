#######此文件将收集各种getHTML的方法

import urllib.request as urllib2#即python2的urllib2
import requests
import random
from bs4 import BeautifulSoup

headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection':'keep-alive',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
       }


#using urllib2 不使用代理
def GetHtml_1(url, encode = "utf-8"):
    request = urllib2.Request(url, headers = headers)
    response = urllib2.urlopen(request)#这是一个 对象
    html = response.read()#无法显示中文
    html = html.decode(encode)
    #会出现该错误
    #'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte
    #但将headers中的   'Accept-Encoding':'gzip, deflate'删掉错误就会消失
    #原理：若有上句，则服务器传过来压缩过的数据，需要额外的deflate算法来解压。
    return html

#using urllib2 使用代理
def GetHtml_3(url, encode = "utf-8"):
    #get ipPool
    ipPool = GetIpPool()
    proxy_support = urllib2.ProxyHandler({'http':ipPool[random.randint(0, len(ipPool))]}) #随机选择ip代理
    opener = urllib2.build_opener(proxy_support)
    opener.add_headers=[('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
        ('Connection','keep-alive'),
        ('Accept-Language','zh-CN,zh;q=0.8'),
        ('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0')
       ]
    urllib2.install_opener(opener)

    res = urllib2.urlopen(url)
    html = res.read().decode("utf-8")
    print(html)
    return html

#using requests
def GetHtml_2(url, encode="utf-8"):
    timeout = random.choice(range(80, 155))
    i=0
    while True:
        try:
            req = requests.get(url = url, headers = headers, timeout = timeout)
            break
        except Exception as e:
            print(e)
            time.sleep(random.choice(range(3, 8)))
        i+=1
        if i>20:
            print("connection failed.....")
            print("-------------END-----------")
            break

    return req.content.decode(encode)



#从ip网站爬取ip并检验ip是否可用
#代理速度慢的可以
def GetIpPool():
    #爬取ip
    url = "https://www.xicidaili.com/nt"
    html= GetHtml_1(url, "utf-8")
    bs = BeautifulSoup(html,'html.parser')#standard library
    table = bs.find("table", {'id':'ip_list'})
    trs = table.findAll("tr")[1:]
    ipList = []
    for tr in trs:
        td = tr.findAll("td")[1:3]
        ipList.append((td[0].text, td[1].text))

    #检验ip是否可用
    ipPool = []
    for (ip, port) in ipList:
        proxy_support = urllib2.ProxyHandler({'http':'http://%s:%s'%(ip, port)})
        opener = urllib2.build_opener(proxy_support)
        try:
            res = opener.open('http://httpbin.org/ip', timeout=15)
            html = res.read()
            if ip in str(html):
                ipPool.append('http://%s:%s'%(ip, port))
        except urllib2.HTTPError:
            pass
        except urllib2.URLError:
            pass
        except Exception:
            pass