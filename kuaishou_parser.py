#!/usr/bin/python
#coding:utf8
#################################################################
#
#    file: kuaishou_parser.py
#   usage: ./kuaishou_parser.py
#   brief:
#  author: culbertyang
#   email: 879432083@qq.com
# created: 2017-06-27 16:03:26
#
#################################################################

__metaclass__ = type

import re
import sys
import time
import urllib
import urllib2
import random
import codecs

class Parser:
    def __init__(self, id_start, id_end):
        self.id_start = id_start
        self.id_end   = id_end
        self.raw_url  = r"http://www.gifshow.com/user/"

    """
    提取输出文件名
    """
    def get_out_file_name(self):
        return str(self.id_start) + "_" + str(self.id_end) + ".txt"

    """
    解析用户昵称
    """
    def parse_nick_name(self, content):
        nickname_pattern = r"<.*?title>(.*?)<.*?/title.*?>"
        compiled_nickname_pattern = re.compile(nickname_pattern, re.IGNORECASE | re.UNICODE)
        nick_name = compiled_nickname_pattern.findall(content)
        if len(nick_name) > 0:
            return nick_name[0][:-15]
        else:
            return ""

    def parse_page_desc(self, content):
        desc_pattern = r'<meta name=\"twitter:description\".*?content=\"(.*?)\">'
        compiled_desc_pattern = re.compile(desc_pattern, re.IGNORECASE | re.UNICODE | re.DOTALL)
        page_desc = compiled_desc_pattern.findall(content)
        if(len(page_desc) > 0):
            data = page_desc[0]
            data = data.replace('\n', ' ')
            return data
        else:
            return ""

    def parse_fans(self, content):
        fans_pattern = r'<span class=\"fans">(.*?)\s+.*?</span>'
        compiled_fans_pattern = re.compile(fans_pattern, re.IGNORECASE | re.UNICODE | re.DOTALL)
        fans = compiled_fans_pattern.findall(content)
        if len(fans) > 0:
            return fans[0]
        else:
            return "0"

    def parse_follows(self, content):
        follow_pattern = r'<span class=\"follows">(.*?)\s+.*?</span>'
        compiled_follow_pattern = re.compile(follow_pattern, re.IGNORECASE | re.UNICODE | re.DOTALL)
        follows = compiled_follow_pattern.findall(content)
        if(len(follows) > 0):
            return follows[0]
        else:
            return "0"

    def parse_works(self, content):
        works_pattern = r'<div class=\"user_photos_hd count\">(.*?)\s+.*?</div>'
        compiled_works_pattern = re.compile(works_pattern, re.IGNORECASE | re.UNICODE | re.DOTALL)
        works = compiled_works_pattern.findall(content)
        if(len(works) > 0):
            return works[0]
        else:
            return "0"

    def do_parser(self, header):
        parser_proxy_support = urllib2.ProxyHandler({"http":"http://www.baidu.com:8080"})
        parser_opener        = urllib2.build_opener(parser_proxy_support)
        urllib2.install_opener(parser_opener)

        id_start = int(self.id_start)
        id_end   = int(self.id_end)

        output_file_name = self.get_out_file_name()
        fdWriter = open(output_file_name, 'w')

        while id_start <= id_end:
            output_line = ""
            parser_url = self.raw_url + str(id_start)
            parser_request = urllib2.Request(parser_url, headers = header)
            try:
                page_data = urllib2.urlopen(parser_request).read()
            except urllib2.HTTPError , e:
                print e.getcode()
                print e.geturl()
                id_start = id_start + 1
                continue

            """
            解析昵称
            """
            nick_name = self.parse_nick_name(page_data)

            """
            解析主页描述
            page_desc = self.parse_page_desc(page_data)
            """

            """
            解析粉丝数
            """
            fans = self.parse_fans(page_data)

            """
            解析关注数
            """
            follows = self.parse_follows(page_data)

            """
            解析作品数
            """
            works = self.parse_works(page_data)

            output_line = str(id_start) + "\t" + fans + "\t" + follows + "\t" + works + "\t" + nick_name + "\n"
            fdWriter.write(output_line)
            id_start = id_start + 1
            #time.sleep(random.randint(2, 4))
        fdWriter.close()


if __name__ == "__main__":

    """
    输入起始id和结束id
    """
    if (len(sys.argv) < 3):
        print 'you  should input id_start and id_end'
        exit(1)

    if not (re.match(r'\d+$', sys.argv[1]) and re.match(r'\d+$', sys.argv[2])):
        print 'id_start and id_end should be  integer'
        exit(1)

    if long(sys.argv[1]) > long(sys.argv[2]):
        print 'id_start should be smaller than id_end'
        exit(1)


    """
    构造请求header
    """
    page_header = {}
    page_header["Accept"] = r'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    #page_header["Accept-Encoding"] = r'gzip, deflate, sdch'
    page_header["Accept-Language"] = r'zh-CN,zh;q=0.8'
    page_header["Cache-Control"]   = r'max-age=0'
    page_header["Cookie"]          = r'aliyungf_tc=AQAAAKSrLwwoeAAAIRYRDqslD/cBr1rt; did=web_c34667aac1d596acd1d6ad65b5755c79; logj=; Hm_lvt_86a27b7db2c5c0ae37fee4a8a35033ee=1498547989; Hm_lpvt_86a27b7db2c5c0ae37fee4a8a35033ee=1498550144'
    page_header["Host"]            = r'www.gifshow.com'
    page_header["Proxy-Connection"]= r'keep-alive'
    page_header["Upgrade-Insecure-Requests"] = r'1'
    page_header["User-Agent"] = r'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    """
    爬取操作
    """
    parseOne = Parser(sys.argv[1], sys.argv[2])
    parseOne.do_parser(page_header)
