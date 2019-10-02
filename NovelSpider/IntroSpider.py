import requests
from bs4 import BeautifulSoup
import gzip
#爬取晋江排行榜的文章及作者，简介，并输入到excel
#@author zyyz
#@version 1.0.0
#@latest update:2019/9/27

def GetHtml(url, encode="utf-8"):
    headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection':'keep-alive',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Accept-Encoding':'gzip, deflat',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
           }
    
    response = requests.get(url, headers = headers, timeout=20)
    #网页太大，会卡住，亟待解决

    html = response.text
    return html


def GetBookList(bs):
    #每类24本
    #<a target="_blank"href="onebook.php?novelid=\d*"
    #<a target="_blank" href="onebook.php?novelid=4055823" alt="陪太子读书" title="陪太子读书">陪太子读书</a>
    a_list = bs.findAll("a", {"target":"_blank"})
    print(a_list)

if __name__ == "__main__":
    url = "http://www.jjwxc.net/topten.php?orderstr=16"
    html = GetHtml(url, "gb2312")
    bs = BeautifulSoup(html, "html.parser")
    book_list = GetBookList(bs)
    
    
