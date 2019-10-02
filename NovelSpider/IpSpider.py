#####get ip from web and save in the file
from GetHtml import GetHtml_1
import re
import msvcrt
import pickle
import hashlib
import base64

#get ip from xicidaili
######using re 正则表达式
def GetIp_xicidaili(url:str):
    html= GetHtml_1(url)
    ip_list = re.findall(r"<td>(\d+\.\d+\.\d+\.\d+)</td>", html)
    proxy_list= re.findall(r"<td>(\d+)</td>", html)
    
    ip = []
    for i in range(0, len(ip_list)):
        ip.append("http://{0}:{1}".format(ip_list[i], proxy_list[i]))

    return ip

def Write2File(ip:list, url:str):
    with open(url, "wb") as f:
        #得到封装的对象
        s = pickle.dumps(ip)
        #对其进行加密
        code = base64.b64encode(s)
        #对其进行加密
        f.write(code)

def DecodeIp(url = "AgencyIp.txt"):
    with open(url, "rb") as f:
        code = f.readlines()
        s = base64.b64decode(code[0])
        ip = pickle.loads(s)
        return ip[0]

if __name__ == "__main__":
    #XiciDaili.com 网站的代理
    url_xicidaili = ["https://www.xicidaili.com/nt", "https://www.xicidaili.com/wn/", "https://www.xicidaili.com/wt/"]

    ip_list=[]
    for url in url_xicidaili:
        ip_list.append(GetIp_xicidaili(url))
        ####加一个检测

    Write2File(ip_list, "AgencyIp.txt")#temporary
    
    print("Ip Spider has finished.")
    msvcrt.getch()
    