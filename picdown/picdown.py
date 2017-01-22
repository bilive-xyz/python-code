#!usr/bin/env python
#!-*- coding:utf-8 -*-

import re
import requests
import os
import time

def downPic(html,keyword):
    pic_url=re.findall(r'"objURL":"(.*?)",',html,re.S)
    i=0
    print '找到关键词: '+keyword+'的图片，现在开始下载...'
    time1 = time.clock()
    for each in pic_url:
        print '正在下载第'+str(i+1)+'张图片，图片地址：'+str(each)
        try:
            pic=requests.get(each,timeout=10)
        except requests.exceptions.ConnectionError:
            print '【错误】当前图片无法下载'
            continue
        if not os.path.exists('F:/pictures'):
            os.makedirs('F:/pictures')
        strs=os.path.join('F:\\pictures',keyword+'_'+str(i)+'.jpg')
        with open(strs.decode('utf-8').encode('cp936'),'wb') as fp:
            fp.write(pic.content)
            fp.close()
            i+=1
    time2=time.clock()
    print time2-time1

if __name__=='__main__':
    word=raw_input("请输入关键字：")
    url='http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word='+word+'&ct=201326592&v=flip'
    result=requests.get(url)
    downPic(result.text,word)
