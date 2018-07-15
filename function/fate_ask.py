# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 16:49:33 2018

@author: 宇星
"""
import re
import requests
import urllib.request
from bs4 import BeautifulSoup

import random

def main():

    messages = '抽塔羅牌4張567'
        
#    if re.match("^抽(塔羅牌|塔羅|tarot)(\d張)?",messages):
#        match = re.match("^抽(塔羅牌|塔羅|tarot)(\d張)?",messages)
#        if match.group(2) == None:
#            print(match.group(1))
#        else:
#            print(match.group(2))

class fate_ask(object):

    def __init__(self):
        self.class_name = 'fate_ask'
        
    def star(self,res):
        url = "http://www.daily-zodiac.com/mobile"
        request = requests.get(url)
        ytcontent = request.content
        soup = BeautifulSoup(ytcontent, "html.parser")
    
        startlist = soup.select("li a")
        for data in startlist:
            if data.select('img')[0]['alt'] ==res:
                sdata = data
                sdata = 'http://www.daily-zodiac.com{}'.format(sdata.get("href"))
                content = self.starcontent(sdata)
        return content  
    
    def starcontent(self,sdata):
        sdata_link = urllib.request.urlopen(sdata)
        soup_today = BeautifulSoup(sdata_link,'html.parser')
        souptoday_data = soup_today.select('ul.today')
        souptext_data = soup_today.select('article')
        #soup3_data = soup2.s
        for today_data in souptoday_data:
            today = today_data.get_text()
        for text_data in souptext_data:
            text = text_data.get_text().strip()
        content = '{}{}'.format(today,text)
        return content

    def ask(self):
        url = "http://wisdomer2002.pixnet.net/blog/post/224560-%E5%AA%BD%E7%A5%96%E7%B1%A4%E8%A9%A960%E9%A6%96"
        request = requests.get(url)
        ytcontent = request.content
        soup = BeautifulSoup(ytcontent, "html.parser")
    
        content = ""
    
        alist = soup.select("div.article-content li a" )
        random.shuffle(alist)
        askdata = alist[0]
    
                                        
        url=askdata.get("href")
        text=askdata.get_text()
    
        content = '{}\n詳解:{}\n\n'.format(text,url)
        
        return content       
    

if __name__ == '__main__':
    main()