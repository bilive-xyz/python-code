#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import threading
import requests
from bs4 import BeautifulSoup

testUrl = "http://ip.chinaz.com/getip.aspx" # 利用IP查询接口
timeout = 5 # 设置超时
threadNumber = 50 # 设置线程数

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
}

'''
获取所有代理IP地址
'''
def getProxyIp():
    proxy = []
    for i in range(1, 5):
        try:
            url = 'http://www.ip181.com/daili/' + str(i)+'.html'
            res=requests.get(url,headers=headers)
            soup = BeautifulSoup(res.text,'html.parser')
            ips = soup.findAll('tr')
            for x in range(1, len(ips)):
                ip = ips[x]
                tds = ip.findAll("td")
                ip_temp = tds[0].contents[0] + ":" + tds[1].contents[0]
                proxy.append(ip_temp)
                print proxy
        except:
            continue
    for i in proxy:
        with open("F:\proxy\proxies.txt", "a+")as f:
            f.write(i+'\n')
            f.close()

getProxyIp()
'''
检测IP是否可用
'''
def testOnline(ip,port):
    global testUrl
    global timeout
    keyWord = ip
    proxies = {"http":"http://"+ip+":"+port}
    try:
        socket.setdefaulttimeout(5)
        res = requests.get(testUrl,proxies=proxies,headers=headers,timeout=timeout).text
        print res
        file=open('F:\proxy\success.txt',"a+")
        file.write(ip+":"+port+"\n")
        file.close()
    except Exception as e:
        print proxy
        print e

class myThread (threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
    def run(self):
        testOnline(self.ip,self.port)

proxies=open('F:\proxy\proxies.txt',"r")
threads = [] # 线程池
for proxy in proxies:
    line = proxy[0:-1]
    ip = line.split(":")[0] # 获取IP
    port = line.split(":")[1]
    threads.append(myThread(ip,port))

for t in threads:
    t.start()
    while True:
        if(len(threading.enumerate())<threadNumber):
            break
