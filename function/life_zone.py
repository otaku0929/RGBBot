# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 17:47:46 2018

@author: 宇星
"""

import requests
import re
import json
from bs4 import BeautifulSoup


def main():

    _life=life_zone()
    messages='天堂M黑妖練等'
    return(_life.gamer(messages))
    
class life_zone(object):
    
    def __init__(self):
        self.class_name = 'life_zone'
    
    #巴哈姆特    
    def gamer(self,res):
    
        s_url = 'https://www.googleapis.com/customsearch/v1element'
        payload = {
               'key':'AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY',
                'cx':'partner-pub-9012069346306566:kd3hd85io9c',
                'q': res,
                'cse_tok': 'AF14hljhr7Db4l8Sce_AXfC9IO6BAlnjaA:1530609483589'
                }
        _json = requests.get(s_url, params=payload)
        json_content = json.loads(_json.content)
        
        #print(json_content)
        game_list = json_content['results']
    
        content = ""
        i = 0
        for obj in game_list:
            _obj = str(obj['richSnippet']['metatags'])
            if re.search('ogUrl',_obj):
                url = obj['richSnippet']['metatags']['ogUrl']
                content = content + url +'\n\n'
                i = i+1;
                if i == 5:
                    return content
                
    #mygopen
    def mygopen(self,res):
        
        ourl ='https://www.mygopen.com/search?q='
        #url = '{}{}'.format(ourl,res.encode('utf-8'))
        url = '{}{}'.format(ourl,res)
        request = requests.get(url)
        soup = BeautifulSoup(request.content, "html.parser")
        soup_content0 = soup.select("article[class='post hentry']")
        soup_content = soup.select("div[class='img-thumbnail']")
        return_obj = ""
        i = 0
        
        if len(soup_content) == 0:
            return "查無相關資料,請更新關鍵字或至https://www.mygopen.com登錄流言"    
        else:
            for obj in soup_content0:
              content = obj.select("a")[1].get('href')
              return_obj = '{}\n{}'.format(return_obj,content)
              i += 1;
              if i == 5:
                  return '{}\n{}\n\n{}'.format("MyGoPen Say:",return_obj,'*超過5筆，僅列出前5筆*\n請共同抵制假消息')            
        
            return '{}\n{}\n\n{}'.format("MyGoPen Say:",return_obj,'請共同抵制假消息')        
    

if __name__ == '__main__':
    main()