#!usr/bin/env python
# -*- coding:utf-8 -*-

import urllib2
import sys

class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None
        try:
            response=urllib2.urlopen(url)
        except urllib2.URLError as e:
            if hasattr(e, "code"):
                print "Error code: %s" % e.code
            elif hasattr(e, "reason"):
                print "Reason: %s" % e.reason
            sys.exit(2)
            if response.getcode() != 200:
                return None
        return response.read()