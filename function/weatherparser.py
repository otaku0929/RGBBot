# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 23:09:59 2018

@author: 宇星
"""
#import os
import requests
import json
import re
import math
from bs4 import BeautifulSoup
import urllib.request

import function.sql
_sql = function.sql.Sql()

import function.g_function
_function = function.g_function.function()

import function.photo_zone
_photos = function.photo_zone.photo_zone()

def main():
    wp = WeatherParser()
    print(wp.AQI())
    #print(wp.getReportWithAPI('龜山'))
#    messages = '查天氣=基隆'
#    match = re.match('(.+)*天氣=(.+)',messages)
#    loc = match.group(2)
#    #print(loc)
#    #locA =  gfunction.getGeoForAddress(loc)
#    #wp_state = get_state(locA,'wp')
#    #print(wp_name['state_name'])
#    #print(wp_location)
#    #print(wp_state)
#    #wp_content = (wp.getReportWithAPI(wp_state['state_name']))
#    wp_content = wp.getReportWithAPI(loc)
#    content = '地點:{}\n{}'.format(loc,wp_content)
#    print(content)

class WeatherParser(object):
    
    def __init__(self):
        self.doc_name_C0 = "O-A0001-001"#"F-C0032-001"
        self.doc_name_46 = "O-A0003-001"
        self.doc_name_FC32 = "F-C0032-001"
        self.user_key = "CWB-A01FD046-AA6B-4C27-A307-616C33DB89B7"
        #self.api_link = "http://opendata.cwb.gov.tw/opendataapi?dataid=%s&authorizationkey=%s" % (self.doc_name,self.user_key)
        self.wp_state_json = '..\\json_file\\wp_state.json'
        self.wp_id = 'w001'

    def get_state_json(self):
        select_command = "select json_file from system_json where id = '%s'"% self.wp_id
        return(_sql.select(select_command))
    
    
    def wp_state_to_db(self):
        wp_json = self.get_wp_state()
        json_file = json.dumps(wp_json)
        id = self.wp_id
        json_name = 'wp_state'
        select_command = "select * from system_json where id = '%s'"% id
        if len(_sql.select(select_command)) == 0:
            sql_command = "insert into system_json (id,json_name,json_file) values('%s','%s','%s')" % (id,json_name,json_file)
            _sql.run(sql_command)
            return 'commit'
        else:
            sql_command = "update system_json set json_file = '%s' where id = '%s'" % (id,json_file)
            _sql.run(sql_command)
            return 'commit'
            
        #return(_sql.select(select_command))
        #return(wp_json)
    
    def get_wp_state(self):
        
        url = "http://e-service.cwb.gov.tw/wdps/obs/state.htm#%E7%8F%BE%E5%AD%98%E6%B8%AC%E7%AB%99"
        request = requests.get(url)
        soup = BeautifulSoup(request.content, "html.parser")
        
        wp_state_list = {}
        for table_row in soup.select('table tr'):
            cells = table_row.findAll('td')
            if len(cells)>0:
                state_no = cells[0].text.strip()
                state_name = cells[1].text.strip()
                altitude = cells[2].text.strip()
                loc_x = cells[3].text.strip()
                loc_y = cells[4].text.strip()
                city = cells[5].text.strip()
                addr = cells[6].text.strip()
                if len(state_no) == 6:
                    wp_state = {state_no:{
                                        'state_no':state_no,
                                        'state_name':state_name,
                                        'altitude':altitude,
                                        'loc_x':loc_x,
                                        'loc_y':loc_y,
                                        'city':city,
                                        'addr':addr                 
                                    }
                                }
                    wp_state_list.update(wp_state)
        return wp_state_list
    
    def get_state(self, locA, stype):
        
        wps_json = self.get_state_json()       
        wps=json.loads(wps_json[0][0])
        
        if stype == 'wp':
            match_key = '^(C0|46)(.+)'
        elif stype == 'rain':
            match_key = '^C1(.+)'
    
        get_dis_list ={}
        for obj in wps:
            locA_x = locA[1]  #經度
            locA_y = locA[0]  #緯度
            locB_x = wps[obj]['loc_x'] #經度
            locB_y = wps[obj]['loc_y'] #緯度
            distant =  _function.getDistance(locA_y,locA_x,locB_y,locB_x)
            if distant <10:
                if re.match(match_key,obj):
                    get_dis_list.update({distant:obj})  
        
        #print(get_dis_list)
        
        dis_list =[]
        for obj in get_dis_list:
            dis_list.append(obj)
        dis_list.sort()
    
        wp_list = []
        for obj in dis_list:
            wp_list.append(wps[get_dis_list[obj]])
        
        #return (wps[get_dis_list[dis_list[0]]])
        return wp_list
        
    def getReportWithAPI(self, location):
        
        locA =  _function.getGeoForAddress(location)

        if locA == "ZERO_RESULTS":
            return "查不到座標位置，請重新提供關鍵字"

        wp_state = self.get_state(locA,'wp')
        #print(wp_state)
        
        for obj in wp_state:
            #wp_no = obj['state_no']
            wp_loc = obj['state_name']
            if re.match('^46(.+)',obj['state_no']):
                doc_name = self.doc_name_46
            elif re.match('^C0(.+)',obj['state_no']):
                doc_name = self.doc_name_C0

            headers = {'Authorization': self.user_key}
            url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/%s?locationName=%s' % (doc_name, wp_loc)
            res = requests.get(url, headers=headers)
            wp_json = res.json()

            #ELEV 高度 公尺
            #WDIR 風向 度
            #WDSD 風速 公尺/秒
            #TEMP 溫度 攝氏
            #HUMD 濕度 %
            #PRES 氣壓 百帕
            #SUN 日照時數 
            #H_24R 日累積雨量 毫米
            #WS15M
            #WD15M
            #WS15T
            #D_TX 本日最高溫   #D_TXT 本日最低溫時間
            #D_TN 本日最低溫   #D_TNT 本日最低溫時間
            #CITY_SN 縣市編號  #TOWN_SN 鄉鎮編號
 
            if len(wp_json['records']['location']) > 0:
                TIME = wp_json['records']['location'][0]['time']['obsTime']
                _WDIR = float(wp_json['records']['location'][0]['weatherElement'][2]['elementValue'])
                WDIR = _function.degToCompass(_WDIR)
                WDSD = wp_json['records']['location'][0]['weatherElement'][2]['elementValue']
                TEMP = round(float(wp_json['records']['location'][0]['weatherElement'][3]['elementValue']),1)
                HUMD = round(float(wp_json['records']['location'][0]['weatherElement'][4]['elementValue'])*100)
                H_24R = wp_json['records']['location'][0]['weatherElement'][7]['elementValue']
                #D_TX = wp_json['records']['location'][0]['weatherElement'][14]['elementValue']
                #D_TN = wp_json['records']['location'][0]['weatherElement'][16]['elementValue']
         
                e = float(HUMD)/100*6.105*math.exp(17.27*float(TEMP)/(237.7+float(TEMP)))      
                AT = round(1.07*float(TEMP)+0.2*e-0.65*float(WDSD)-2.7,1)
                
                content = '觀測站：{}\n時間：{}\n溫度：{}°C\n體感溫度：{}°C\n濕度：{}%\n風向：{}\n風速：{} m/s\n日累積雨量：{} 毫米\n-------------------\n資料來源：中央氣象局'.format(wp_loc,TIME[5:16],TEMP,AT,HUMD,WDIR,WDSD,H_24R)
                return content 
        
    def weather(self,location):

        #api_link = "http://opendata.cwb.gov.tw/opendataapi?dataid=%s&authorizationkey=%s" % (self.doc_name_FC32,self.user_key)
       
        headers = {'Authorization': self.user_key}
        res = requests.get("http://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?locationName=%s" % location,headers=headers)
        weather_api= res.json()
    
        weather_elements = weather_api['records']['location'][0]['weatherElement']
        
        #sTs = (weather_elements[0]['time'])[0].get('startTime')[5:16]
        #eTs = (weather_elements[0]['time'])[0].get('endTime')[5:16]
        Wxs = (weather_elements[0]['time'])[0]['parameter'].get('parameterName')
        PoPs = (weather_elements[1]['time'])[0]['parameter'].get('parameterName')
        MinTs = (weather_elements[2]['time'])[0]['parameter'].get('parameterName')
        MaxTs = (weather_elements[4]['time'])[0]['parameter'].get('parameterName')
    
        #sTe = (weather_elements[0]['time'])[1].get('startTime')[5:16]
        #eTe = (weather_elements[0]['time'])[1].get('endTime')[5:16]
        Wxe = (weather_elements[0]['time'])[1]['parameter'].get('parameterName')
        PoPe = (weather_elements[1]['time'])[1]['parameter'].get('parameterName')
        MinTe = (weather_elements[2]['time'])[1]['parameter'].get('parameterName')
        MaxTe = (weather_elements[4]['time'])[1]['parameter'].get('parameterName')
    
        if Wxs == Wxe:
            Wx = '{}'.format(Wxs)
        else:
            Wx = '{} 轉 {}'.format(Wxs,Wxe)
    
        if PoPs > PoPe:
            PoP = '降雨機率:{}%~{}%'.format(PoPe,PoPs)
        elif PoPs < PoPe:
            PoP = '降雨機率:{}%~{}%'.format(PoPs,PoPe)
        else:
            PoP = '降雨機率:{}%'.format(PoPs)
    
        if MinTs < MinTe:
            MinT = MinTs
        elif MinTs > MinTe:
            MinT = MinTe
        else:
            MinT = MinTs
    
        if MaxTs < MaxTe:
            MaxT = MaxTe
        elif MaxTs > MaxTe:
            MaxT = MaxTs
        else:
            MaxT = MaxTs
            
    
        #content1 = '{}\n時間:{}~{}\n天氣:{}\n溫度:{}C~{}C\n降雨機率:{}%'.format(location,sTs,eTs,Wxs,MinTs,MaxTs,PoPs)
        #content2 = '時間:{}~{}\n天氣:{}\n溫度:{}C~{}C\n降雨機率:{}%'.format(sTe,eTe,Wxe,MinTe,MaxTe,PoPe)
    
        _content3 = '{}\n{}\n溫度:{}C~{}C\n{}'.format(location,Wx,MinT,MaxT,PoP)
    
        #content = '{}\n\n{}'.format(content1,content2)
       
        return _content3

    def ty(self):
    
        src = 'http://www.cwb.gov.tw/V7/prevent/typhoon/Data/PTA_NEW/index.htm?dumm=Wed#'
        url = urllib.request.urlopen(src)
        soup = BeautifulSoup(url, 'html.parser')
        data = soup.select('div.patch')
        text = data[0].get_text().strip()
        #imgsoure = soup.select('div.download a')
    
        #imgurl = imgsoure[0].get('href')
        #imglink = 'http://www.cwb.gov.tw/V7/prevent/typhoon/Data/PTA_NEW/{}'.format(imgurl)
    
        content = '台灣附近颱風動態：\n{}'.format(text)
    
        return content

    def AQI(self):
        path = 'jpg/'
        #path = '../jpg/'
        aqi_path = '%sapi_map_png'%path
        aqi_detail_path = '%saqi.png'%path
        merge_path = '%smerge_aqi.png'%path
        aqi_url = 'https://taqm.epa.gov.tw/taqm/Chart/AqiMap/map2.aspx?lang=tw'
        with open(aqi_path, 'wb') as handle:
            aqi_pic = requests.get(aqi_url, stream=True)
            handle.write(aqi_pic.content)
        _function.mergejpg_h(aqi_path,aqi_detail_path,merge_path)
#        client = ImgurClient(imgur_client_id, imgur_client_secret, imgur_client_access_token, imgur_client_refresh_token)
#        conf = {"album":'sJMh0RE'}
#        res = client.upload_from_path('/app/jpg/merge_aqi.png',config=conf,anon=False)
        res = _photos.upload_imgur('sJMh0RE',merge_path)
        
        return res
    
if __name__ == '__main__':
    main()