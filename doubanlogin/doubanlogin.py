#!usr/bin/env python
#!-*- coding:utf-8 -*-

import cookielib
import urllib,urllib2
import re

import sys


class DouBan():
    def __init__(self):
        #登陆页面
        self.login_url = "https://accounts.douban.com/login"
        #创建一个cookie对象
        self.cookies = cookielib.CookieJar()
        #构建opener
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        #伪造header
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'}
        #构造post数据
        self.data = {'captcha-id': '',
                     'captcha-solution': '',
                     'form_email': '你的邮箱',
                     'form_password': '你的密码',
                     'login': '登录',
                     'redir': 'https://www.douban.com/',
                     'source': 'index_nav'}

    def get_captcha(self):
        login_page = self.opener.open('https://www.douban.com/accounts/login?source=main').read()
        #提取captcha-id的值
        capid = re.search('<input type="hidden" name="captcha-id" value="(.*?)"/>', login_page)
        self.data['captcha-id'] = capid.group(1)
        #提取验证码url地址
        imgurl = re.search('<img id="captcha_image" src="(.*?)" alt="captcha" class="captcha_image"/>', login_page)
        if imgurl:
            url = imgurl.group(1)
            urllib.urlretrieve(url, 'v.jpg')

    def login(self):
        print "请输入验证码："
        cap = raw_input('input :')
        self.data['captcha-solution'] = cap
        #利用urlencode转换编码
        post_data = urllib.urlencode(self.data)
        #构建request请求
        request = urllib2.Request(self.login_url, post_data, headers=self.header)
        urllib2.install_opener(self.opener)
        try:
            response=urllib2.urlopen(request)
        except urllib2.URLError as e:
            if hasattr(e, "code"):
                print "Error code: %s" % e.code
            elif hasattr(e, "reason"):
                print "Reason: %s" % e.reason
            sys.exit(2)
        result = response.read()
        print result

if __name__=='__main__':
    douban = DouBan()
    douban.get_captcha()
    douban.login()