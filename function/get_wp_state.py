# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 23:25:35 2018

@author: 宇星
"""

import json
import requests
from bs4 import BeautifulSoup
import re

import function.g_function
gfunction = function.g_function.function()



wp_state_json = '..\\json_file\\wp_state.json'

def main():
       
    #locA = gfunction.getGeoForAddress('中和興南夜市')
    print(get_state(locA, 'C0'))
    #print(update_wp_dict())

def get_state(locA, stype):
    
    wps=rd_json()
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
        distant =  gfunction.getDistance(locA_y,locA_x,locB_y,locB_x)
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
    
def get_wp_state():
    
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

def update_wp_dict():
    wt_json(get_wp_state())
    return('wt_OK')

def rd_json():

    with open(wp_state_json, encoding='CP950') as jsonfile:
        #print(jsonfile)
        
        data = json.load(jsonfile)
        return(data)
   
    
def wt_json(data):   

    with open(wp_state_json, 'w') as outfile:  
        json.dump(data, outfile ,ensure_ascii=False,indent=2)
    
    return "OK"

def wt(data):
    f=open('wp.txt','w', encoding='UTF-8')
    f.write(format(data))
    f.close()
    #print ('--print ok--')   
    

if __name__ == '__main__':
    main()