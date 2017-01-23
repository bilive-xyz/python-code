#!usr/bin/env python
#!-*- coding:utf-8 -*-
import multiprocessing
import random
import string
import requests,re,os
import time


def down(url):
    try:
        pic = requests.get(url, timeout=10)
    except requests.exceptions.ConnectionError:
        print '【错误】当前图片无法下载'
    name = ''.join(random.choice(string.letters + string.digits) for i in xrange(5))
    print '正在下载图片%s:' % name
    if not os.path.exists('F:/pictures'):
        os.makedirs('F:/pictures')
    strs = os.path.join('F:\\pictures',"img" + '_' + str(name) + '.jpg')
    with open(strs.decode('utf-8').encode('cp936'), 'wb+') as fp:
        fp.write(pic.content)
        fp.close()

def main(urls):
    t_start=time.time()
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    for url in urls:
        pool.apply_async(down, args=(url,))
    pool.close()
    pool.join()
    pool.terminate()
    t_end=time.time()
    t=t_end-t_start
    print 'the program time is :%s' %t

if __name__=='__main__':
    word = raw_input("请输入关键字：")
    url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + word + '&ct=201326592&v=flip'
    result = requests.get(url)
    urls = re.findall(r'"objURL":"(.*?)",', result.text, re.S)
    main(urls)


