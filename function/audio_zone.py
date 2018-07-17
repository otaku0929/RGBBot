# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 15:16:36 2018

@author: 宇星
"""

import requests
from bs4 import BeautifulSoup

def main():
    print('ok')
    
class audio_zone(object):
    def __init__(self):
        self.class_name = 'audio_zone'
        
    def youtube_search(self,res):
    
         url="https://www.youtube.com/results?search_query={}".format(res)
         request = requests.get(url)
         ytcontent = request.content
         soup = BeautifulSoup(ytcontent, "html.parser")
        
         content = ""
    
         all_mv = soup.select("a[class='yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link ']")
         mvlist = all_mv[0]
    
         url="https://www.youtube.com{}".format(mvlist.get("href"))
         title=mvlist.get("title")
    
         content='{}\n{}'.format(title,url)
    
         return content

if __name__ == '__main__':
    main()