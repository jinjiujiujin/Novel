#######此文件将收集各种getHTML的方法

import urllib.request as urllib2#即python2的urllib2
import requests
import random
from retrying import retry
from bs4 import BeautifulSoup

headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection':'keep-alive',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
       }
       
ip_pool = ["http://163.125.148.91:9999", "https://61.128.208.94:3128", "http://59.44.247.194:9797", "http://120.25.253.234:8118", "https://218.60.8.83:3129", "http://58.243.50.184:53281"]


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

def getHeaders():
    user_agent_list = [ \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" 
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", 
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", 
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", 
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", 
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", 
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", 
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", 
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", 
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", 
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", 
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", 
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", 
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", 
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", 
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", 
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", 
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
    ]
    UserAgent=random.choice(user_agent_list)
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection':'keep-alive',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'User-Agent':UserAgent
       }
    return headers


#using requests
@retry(stop_max_attempt_number=3)
def GetHtml_2(url, timeout=-1):
    proxy = random.choice(ip_pool)
    if timeout == -1:
        timeout = random.choice(range(8, 15))
    try:
        #standard format e.g. {"http":"163.125.148.91:9999"}
        proxies = {proxy[:proxy.find(":")] : proxy[proxy.find(":")+3:]}
        response = requests.get(url, headers = getHeaders(), proxies = proxies, timeout = timeout)
        content = response.text
        return content
    except Exception as http:
        print(" [-] Error:", http)
        if timeout > 12:
            ip_pool.remove(proxy)
            print(" [-] Removed proxy ", proxy)
        return None


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
