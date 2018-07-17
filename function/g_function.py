# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 22:58:43 2018

@author: 宇星
"""
import os
import json
import requests
#import urllib
#from urllib.request import urlopen
import math
from PIL import Image, ImageFont, ImageDraw, ImageColor
#from imgurpython import ImgurClient
#
#imgur_client_id = '33ed33e765afedc'
#imgur_client_secret = '04f0d5531b1d0978ff97fd990554c899e9e7e1f5'
#imgur_client_access_token = '85b737858a3ca32f1517bd9b8e2f5d2c5c97a647'
#imgur_client_refresh_token = '797c2292b2600815f93cc73bec6eb7c8bdbcd67e'
#album_id = 'sJMh0RE'

def main():
    #print(get_hsing())
    gfunction = function()
    #print (gfunction.getDistance('121.7812','25.0712','21.4420','24.9976'))
    print(gfunction.imgur_images_delete('AZL5bX9'))

class function(object):
    
    def __init__(self):
        self.name = 'start'

    def is_number(self,string):
        try:
            float(string)
            return True
        except ValueError:
            pass
         
        try:
            import unicodedata
            unicodedata.numeric(string)
            return True
        except (TypeError, ValueError):
            pass
         
        return False
    

    def wt_json(self, data, filename):   
    
        with open(filename, 'w') as outfile:  
            json.dump(data, outfile ,ensure_ascii=False,indent=2)
            
        return True
    
    def rd_json(self, filename):
    
        with open(filename) as json_file:  
            data = json.load(json_file)
            return(data)
        
    def getGeoForAddress_json(self,address):
        s_url = 'http://maps.googleapis.com/maps/api/geocode/json'
        payload ={'address':address}
        _json = requests.get(s_url, params=payload)
        return json.loads(_json.content)

    def getGeoForAddress(self,address):

        responseJson = self.getGeoForAddress_json(address)
        status = responseJson['status']
        
        if status == "ZERO_RESULTS":
            return "ZERO_RESULTS"
        
        while status == 'OVER_QUERY_LIMIT':
            responseJson = self.getGeoForAddress_json(address)
            status = responseJson['status']
            if status == "OK":
                Lat = responseJson['results'][0]['geometry']['location']['lat']
                Lng = responseJson['results'][0]['geometry']['location']['lng']
                return [Lat,Lng]
                break
        
        Lat = responseJson['results'][0]['geometry']['location']['lat']
        Lng = responseJson['results'][0]['geometry']['location']['lng']
        return [Lat,Lng]
      
    def getDistance(self,lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
        """
        根据经纬度计算距离
        :param lon1: 点1经度
        :param lat1: 点1纬度
        :param lon2: 点2经度
        :param lat2: 点2纬度
        :return:distance
        """
        # 将十进制度数转化为弧度
        lon1, lat1, lon2, lat2 = map(math.radians, [float(lon1), float(lat1), float(lon2), float(lat2)])
    
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371.137  # 地球平均半径，单位为公里
        return float('%.2f' % (c * r))

    def degToCompass(self,num):
        val=int((num/22.5)+.5)
        #arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
        arr=['北','北北東','東北','東北東','東','東南東','東南','南南東','南','南南西','西南','西南西','西','西北西','西北','北北西']
        return arr[(val % 16)]
    
    def mergejpg_h(self,p1,p2,output):
        
        path = 'jpg/'
        #path = '../jpg/'
        temp_path = '%sresized.jpg'%path        
        merge_path = '%smerge_aqi.png'%path

        
        img1 = Image.open(p1)
        img2 = Image.open(p2)
        w1,h1 = img1.size
        w2,h2 = img2.size
        
        #resized = im2.resize((w1,))
        _h=int(float(w1)/float(w2)*h2)
        nim = img2.resize((w1,_h),Image.BILINEAR)
        nim.save(temp_path)
        
        mh= h1+_h
        merge_img = Image.new('RGB', (w1, mh), 0xffffff)
        i=0
        merge_img.paste(img1, (0, i))
        merge_img.paste(nim, (0, i+h1))
    
        #merge_img.save(output)
        merge_img.save(merge_path)   
        
        return ("merge_OK")
    
    def add_watermark(self, text, fontsize, ttf, color, alpha, position, imagefile, output_dir):
        
        ttf_path='font/'
        #ttf_path='/app/font/'
        
        ttf_dict={'t1':'wt014.ttf',
                  't2':'wt028.ttf',
                  't3':'wt040.ttf',
                  't4':'wt064.ttf',
                  't5':'wt071.ttf',
                  't6':'c01W4.ttc',
                  't7':'c02W3.ttc',
                  'e1':'e1.ttf',
                  'e2':'e2.ttf',
                  'e3':'e3.ttf',
                  'e4':'e4.ttf',
                  }
        
        ttf_name = ttf_dict[ttf]
        
        fontname = '%s%s'%(ttf_path,ttf_name)
        #print(fontname)
             
        #set font color
        if color == 'red':
            r=255;g=0;b=0
        elif color == 'green':
            r=0;g=255;b=0
        elif color == 'blue':
            r=0;g=0;b=255
        elif color == 'white':
            r=255;g=255;b=255
        elif color == 'black':
            r=0;g=0;b=0
        elif color == 'yellow':
            r, g, b = ImageColor.getrgb("#ffff00")
        elif color == 'pink':
            r, g, b = ImageColor.getrgb("#ffc0cb")
        elif color == 'gold':
            r, g, b = ImageColor.getrgb("#ffd700")
        else:
            r, g, b = ImageColor.getrgb(color)
            #print(r,g,b)
              
            
        img0 = Image.new("RGBA", (1,1))
        draw0 = ImageDraw.Draw(img0)
        font = ImageFont.truetype(fontname, fontsize)
        t_width, t_height = draw0.textsize(text, font=font)
        #t_width, t_height = draw0.textsize(unicode(text, 'UTF-8'), font=font)
        img = Image.new("RGBA", (t_width, t_height), (255,0,0,0))
        draw = ImageDraw.Draw(img)
        #draw.text((0,0),unicode(text, 'UTF-8'), font=font, fill=(255,255,255,128))
        draw.text((0,0),text,font=font, fill=(r,g,b,alpha))
        img2 = Image.open(imagefile)
        i_width, i_height = img2.size
        
        if position == 'p1':
            px = int(i_width*(1/15))
            py = int(i_height*(1/15))
        elif position == 'p2':
            px = int(i_width*(1/15))
            py = int((i_height-t_height)/2)
        elif position == 'p3':
            px = int(i_width*(1/15))
            py = int((i_height-t_height)*(14/15))
        elif position == 'p4':
            px = int((i_width-t_width)/2)
            py = int(i_height*(1/15))
        elif position == 'p5':
            px = int((i_width-t_width)/2)
            py = int((i_height-t_height)/2)
        elif position == 'p6':
            px = int((i_width-t_width)/2)
            py = int(i_height*(14/15))
        elif position == 'p7':
            px = int((i_width-t_width)*(14/15))
            py = int(i_height*(1/15))
        elif position == 'p8':
            px = int((i_width-t_width)*(14/15))
            py = int((i_height-t_height)/2)
        elif position == 'p9':
            px = int((i_width-t_width)*(14/15))
            py = int((i_height-t_height)*(14/15))
    
        img2.paste(img, (px, py), img)
        imagefile = imagefile.split('/')[-1]
        imagefile = "wm_" + imagefile
        print (imagefile + " saved...")
        img2.save(output_dir + imagefile)
        del draw0, draw
        del img0, img, img2
        
        return 'OK'
    
    
#def get_hsing():
#    return s17api.hsing.getjson(0,1912544)

if __name__ == '__main__':
    main()

###輸出浮水印
#    uid = 'victor'
#    image_file = '..//jpg//star.jpg'
#    output_dir = '..//jpg//'
#    watermar_json = '..//json_file//watermark_{}.json'.format(uid) 
#    if os.path.exists(watermar_json):
#        with open(watermar_json, encoding='CP950') as jsonfile:
#            data = json.load(jsonfile)
#            text = data['watermark']['text']
#            fontsize = data['watermark']['fontsize']
#            ttf = data['watermark']['ttf']
#            color = data['watermark']['color']
#            alpha = data['watermark']['alpha']
#            position = data['watermark']['position']
#        add_watermark(text, int(fontsize), ttf, color, int(alpha), position, image_file, output_dir)
#    else:
#        print('請先設定浮水印輸出格式，方式如下:\n\
# 浮水印t=小星星浮水印f=52ttf=t4c=whiteal=128p=p9\n\
#  ------------\n\
#  *t=浮水印內容\n\
#  *f=字體大小\n\
#  *ttf=字型：目前共有中文7,英文4種t1~t7 e1~e4 \n\
#  *c=顏色:支援red|green|blue|white|break|pink|yellow|gold, 也可以輸入色票#ffffff\n\
#  *al=透明度:0~255 (建議不要小於128)\n\
#  *p=浮水印位置：以九宮格方式劃分')

#設定浮水印
#    messages = '浮水印t=Star浮水印f=72ttf=e3c=redal=255p=p9'
#    #if re.match('浮水印t=(.+)f=(\d+)',messages):
#    if re.match('浮水印t=(.+)f=(\d+)ttf=([t|e]\d)c=(red|green|blue|white|break|pink|yellow|gold|#......)al=(\d+)p=(p\d)',messages):
#        match =  re.match('浮水印t=(.+)f=(\d+)ttf=([t|e]\d)c=(red|green|blue|white|break|pink|yellow|gold|#......)al=(\d+)p=(p\d)',messages)
#        #print (match.group(0))
#        set_watermark('victor',match.group(1),match.group(2),match.group(3),match.group(4),match.group(5),match.group(6))
#    else:
#        print('請先設定浮水印輸出格式，方式如下:\n\
# 浮水印t=小星星浮水印f=52ttf=t4c=whiteal=128p=p9\n\
#  ------------\n\
#  *t=浮水印內容\n\
#  *f=字體大小\n\
#  *ttf=字型：目前共有中文7,英文4種t1~t7 e1~e4 \n\
#  *c=顏色:支援red|green|blue|white|break|pink|yellow|gold, 也可以輸入色票#ffffff\n\
#  *al=透明度:0~255 (建議不要小於128)\n\
#  *p=浮水印位置：以九宮格方式劃分')
