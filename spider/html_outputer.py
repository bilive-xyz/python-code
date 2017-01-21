#!usr/bin/env python
# -*- coding:utf-8 -*-


class HtmlOutputer(object):
    def __init__(self):
        self.datas=[]

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        with open('output.txt','w') as fout:
            for data in self.datas:
                fout.writelines('%s\n' %data['title'].encode('utf-8'))
                fout.writelines('%s\n\n\n' %data['summary'].encode('utf-8'))