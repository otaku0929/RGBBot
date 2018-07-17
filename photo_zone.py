# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 00:32:14 2018

@author: 宇星
"""

import requests
import random
import json
import os
from imgurpython import ImgurClient

import function.sql
_sql = function.sql.Sql()

import function.g_function
_function = function.g_function.function()

from linebot.models import (
        MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)


def main():
    #return 'ok'
    _photos = photo_zone()
    uid = 'Ud0414e339e9c242b19a2dd22dd1f6189'
    content = _photos.add_watermark(uid)
    print (content)

class photo_zone(object):
    
    def __init__ (self):
        self.obj_name = 'imgur_function'
        self.imgur_client_id = '33ed33e765afedc'
        self.imgur_client_secret = '04f0d5531b1d0978ff97fd990554c899e9e7e1f5'
        self.imgur_client_access_token = '85b737858a3ca32f1517bd9b8e2f5d2c5c97a647'
        self.imgur_client_refresh_token = '797c2292b2600815f93cc73bec6eb7c8bdbcd67e'       
        self.API_Get_Image = 'https://otakujpbweb.herokuapp.com/api/image/random/'
        self.client = ImgurClient(self.imgur_client_id, self.imgur_client_secret, self.imgur_client_access_token, self.imgur_client_refresh_token)
        
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
        return self.get_imgur_photo('23p2B')
    
    def imgur_boys(self):
        return self.get_imgur_photo('9eQni')       

    def joke(self):
        return self.get_imgur_photo('XpG2g')   
    
    def poker(self):
        return self.get_imgur_photo('KQjab')
    
    def gods_talk(self):
        return self.get_imgur_photo('6FM69')
    
    def single(self):
        return self.get_imgur_photo('Sy6Gm')
    
    def food(self):
        return self.get_imgur_photo('9rYK8')    
    
    def get_imgur_photo(self,album_id):
        client = ImgurClient(self.imgur_client_id, self.imgur_client_secret)
        images = client.get_album_images(album_id)
        index = random.randint(0, len(images) - 1)
        url = images[index].link
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        return image_message
    
    def upload_imgur(self,album_id,path):
        #client = ImgurClient(self.imgur_client_id, self.imgur_client_secret, self.imgur_client_access_token, self.imgur_client_refresh_token)
        conf = {"album":album_id}
        res = self.client.upload_from_path(path,config=conf,anon=False)
        return res

    def imgur_album_images_delete(self,album_id):      
        #client = ImgurClient(imgur_client_id, imgur_client_secret, imgur_client_access_token, imgur_client_refresh_token)
        image_list = self.client.get_album_images(album_id)
        for obj in image_list:
            self.client.delete_image(obj.id)
        
        return ("delete complete")

    def imgur_images_delete(self,image_id):
        
        #client = ImgurClient(imgur_client_id, imgur_client_secret, imgur_client_access_token, imgur_client_refresh_token)
        self.client.delete_image(image_id)
        
        return ("deleted image")

    def add_watermark(self,id,message_content):
        
        select_command = "select * from user_config where user_id = '%s'"% id
        config_json = _sql.select(select_command)[0][2]
        config = json.loads(config_json)      
                
        if config['watermark'] == {}:
            return 'none'
        else:                                   
            path = 'jpg/'
            #path = '../jpg/'
            #path = '/app/jpg/'
            image_file = '%s%s.jpg'%(path,id)
            output_jpg = '%swm_%s.jpg'%(path,id)
            output_dir = path
            
            with open(image_file, 'wb') as fd:
                for chunk in message_content.iter_content():
                    fd.write(chunk)
            
            data = config['watermark']
            #print(data)
            
            text = data['text']
            fontsize = data['fontsize']
            ttf = data['ttf']
            color = data['color']
            alpha = data['alpha']
            position = data['position']
            _function.add_watermark(text, int(fontsize), ttf, color, int(alpha), position, image_file, output_dir)
            res = self.upload_imgur('SZMo93Z',output_jpg)
            return res
        #print(config_json)
        
        #return str(config)
#        watermark_json = '/app/json_file/watermark_{}.json'.format(uid)
#        #print(watermark_json)
#        message_content = line_bot_api.get_message_content(event.message.id)
#        photo_name = event.message.id
#        image_file = '/app/temp_jpg/'+photo_name+'.jpg'
#        output_jpg = '/app/temp_jpg/wm_'+photo_name+'.jpg'
#        output_dir = '/app/temp_jpg/'
#        with open(image_file, 'wb') as fd:
#            for chunk in message_content.iter_content():
#                fd.write(chunk)
#        if os.path.exists(watermark_json):
#            #with open(watermar_json, encoding='CP950') as jsonfile:
#            with open(watermark_json) as jsonfile:
#                data = json.load(jsonfile)
#                print(data)
#                text = data['watermark']['text']
#                fontsize = data['watermark']['fontsize']
#                ttf = data['watermark']['ttf']
#                color = data['watermark']['color']
#                alpha = data['watermark']['alpha']
#                position = data['watermark']['position']
#            _function.add_watermark(text, int(fontsize), ttf, color, int(alpha), position, image_file, output_dir)
#             #_function.add_watermark("小星星浮水印", 58, 't2','p9', image_file, output_dir)
#            client = ImgurClient(imgur_client_id, imgur_client_secret, imgur_client_access_token, imgur_client_refresh_token)
#            conf = {"album":'SZMo93Z'}
#            res = client.upload_from_path(output_jpg,config=conf,anon=False)
#            #print(res)
#            url = res['link']
#            img_id = res['id']
#            del_messages = '下載完圖檔後，請輸入下面指令刪除圖檔 \ndimg={}'.format(img_id)
#            image_message = ImageSendMessage(
#                original_content_url=url,
#                preview_image_url=url
#            )         
#            line_bot_api.reply_message(event.reply_token, [image_message, TextSendMessage(text=del_messages)]) 
#           #gs_write('B30')



if __name__ == '__main__':
    main()