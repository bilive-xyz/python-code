#!usr/bin/env python
#!-*- coding:utf-8 -*-

import threading,Queue
import re,os
import requests
import time

SHARE_Q=Queue.Queue()       #共享队列
_WORKER_THREAD_NUM=4        #线程数
word = raw_input("请输入关键字：")
i = 0
class MyThread(threading.Thread):
    def __init__(self, func):
        super(MyThread, self).__init__()  # 调用父类的构造函数
        self.func = func  # 传入线程函数逻辑

    def run(self):
        self.func()

def work():
    global SHARE_Q
    while not SHARE_Q.empty():
        url=SHARE_Q.get()       #获得任务
        try:
            pic = requests.get(url, timeout=10)
        except requests.exceptions.ConnectionError:
            print '【错误】当前图片无法下载'
        down(pic)
        SHARE_Q.task_done()


def down(pic):
    global i
    global word
    print '正在下载第' + str(i + 1) + '张图片'
    if not os.path.exists('F:/pictures'):
        os.makedirs('F:/pictures')
    strs = os.path.join('F:\\pictures', word + '_' + str(i) + '.jpg')
    with open(strs.decode('utf-8').encode('cp936'), 'wb+') as fp:
        fp.write(pic.content)
        fp.close()
        i += 1

def main():
    global SHARE_Q
    global word
    threads=[]
    url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + word + '&ct=201326592&v=flip'
    result = requests.get(url)
    pic_url = re.findall(r'"objURL":"(.*?)",', result.text, re.S)
    time1=time.time()
    for each in pic_url:
        SHARE_Q.put(each)
    for i in xrange(_WORKER_THREAD_NUM):
        thread=MyThread(work)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    SHARE_Q.join()
    time2=time.time()
    t=time2-time1
    print 'the program time is :%s' %t

if __name__=='__main__':
    main()