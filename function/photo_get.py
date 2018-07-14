# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 00:32:14 2018

@author: 宇星
"""

import requests
import random
from imgurpython import ImgurClient

from linebot.models import (
        MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)


def main():
    return 'ok'

class photo_get(object):
    
    def __init__ (self):
        self.obj_name = 'imgur_function'
        self.imgur_client_id = '33ed33e765afedc'
        self.imgur_client_secret = '04f0d5531b1d0978ff97fd990554c899e9e7e1f5'
        self.imgur_client_access_token = '85b737858a3ca32f1517bd9b8e2f5d2c5c97a647'
        self.imgur_client_refresh_token = '797c2292b2600815f93cc73bec6eb7c8bdbcd67e'       
        self.API_Get_Image = 'https://otakujpbweb.herokuapp.com/api/image/random/'
        
    def random(self):
        b=self.imgur_boys
        g=self.beauty_girls
        gs=self.imgur_girls
        content = random.choice([b,g,b,g,b,g,g,gs])
        return content()
        
                 
    def beauty_girls(self):
        images =  requests.get(self.API_Get_Image)
        url = images.json().get('Url')
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        return image_message
    
    def imgur_girls(self):
        client = ImgurClient(self.imgur_client_id, self.imgur_client_secret)
        images = client.get_album_images('23p2B')
        index = random.randint(0, len(images) - 1)        
        url = images[index].link
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        return image_message
    
    def imgur_boys(self):
        client = ImgurClient(self.imgur_client_id, self.imgur_client_secret)
        images = client.get_album_images('9eQni')
        index = random.randint(0, len(images) - 1)        
        url = images[index].link
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        return image_message  
  

if __name__ == '__main__':
    main()