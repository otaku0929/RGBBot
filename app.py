# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 11:07:15 2018
@author: 宇星
"""

import re
import random
import configparser
import json
import os
#from bs4 import BeautifulSoup
from flask import Flask, request, abort
#from imgurpython import ImgurClient
from function.ifoodie import ifoodie_get

import function.game_zone
_games = function.game_zone.game_zone()

import function.sql
_sql = function.sql.Sql()

import function.config_setting
_config = function.config_setting.config_setting()

import function.sys_messages
_sys_mg = function.sys_messages.sys_messages()

import function.photo_zone
_photos = function.photo_zone.photo_zone()

import function.tarot_detail
_tarot = function.tarot_detail.tarot()

import function.financial
_fin = function.financial.financial()

import function.hsing
_hsing = function.hsing.hsing()

import function.fate_ask
_fate_ask = function.fate_ask.fate_ask()

import function.life_zone
_life = function.life_zone.life_zone()

import function.weatherparser
_weather = function.weatherparser.WeatherParser()

import function.star_talk
_star_talk = function.star_talk.start_talk()

import function.line_function
_lineapi = function.line_function.linbotapi()

import function.g_function
_function =  function.g_function.function()

import function.star_store
_star_store =  function.star_store.star_store()

import function.audio_zone
_audio =  function.audio_zone.audio_zone()

from linebot import (
     LineBotApi, WebhookHandler
)

from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
        MessageEvent,
        ImageMessage,
        TextMessage, 
        TextSendMessage, 
        ImageSendMessage,
        LocationSendMessage
)

app = Flask(__name__)
config = configparser.ConfigParser()
config.read("config.ini")

line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
handler = WebhookHandler(config['line_bot']['Channel_Secret'])

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print("body:",body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'ok'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event",event)
    #print("event.groupID:",event.source)
    #print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    #content = event.message.text
    #line_bot_api.reply_message(event.reply_token,[TextSendMessage(text=str(event)),TextSendMessage(text=content)])
    ####功能區####
    #取得event
    if event.source.type == 'group':
        gid = event.source.group_id
        #print(gid)
        uid = event.source.user_id
        #print(uid)
        #profile = line_bot_api.get_group_member_profile(gid,uid)
        profile = _lineapi.get_group_member_profile(gid,uid)
        #print(profile)
        user_name = profile['displayName']
    if event.source.type == 'user':
        uid = event.source.user_id
        profile = line_bot_api.get_profile(event.source.user_id)
        user_name = profile.display_name
        
    if event.message.text == '#getevent':
        content = event.message.text
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(text=str(event)),TextSendMessage(text=content)])
        return 0
    #取得設定檔
    if event.message.text == '#getinfo':
        if event.source.type == 'group':          
            content = str(profile)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0
        if event.source.type == 'user':
            content = str(profile)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0       
    if event.message.text=='#getconfig':
        if event.source.type == 'user':
            if _sql.select_config(uid) == []:
                content = _sys_mg.m_noconfig(user_name)
                #print(content)
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            else:        
                config = _sql.select_config(uid)
                config_list = config[0]
                #uid=config_list[0]
                #user_name = config_list[1]
                json_data = json.loads(config_list[2])
                content = str(json_data)
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0
        if event.source.type == 'group':
            if _sql.select_config(gid) == []:
                content = _sys_mg.m_noconfig('group')
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            else:
                config = _sql.select_config(gid)
                config_list = config[0]
                json_data = json.loads(config_list[2])
                content = str(json_data)
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
     #user查設定檔
    if event.message.text=='#查小星星設定':
        if event.source.type == 'user':
            if _sql.select_config(uid) == []:
                content = _sys_mg.m_noconfig(user_name)
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            else:        
                config = _sql.select_config(uid)
                config_list = config[0]
                json_data = json.loads(config_list[2])
                content = _config.config_list(json_data)
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0
        if event.source.type == 'group':
            if _sql.select_config(gid) == []:
                content = _sys_mg.m_noconfig('group')
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            else:
                config = _sql.select_config(gid)
                config_list = config[0]
                json_data = json.loads(config_list[2])
                content = _config.config_list(json_data['function_option'])
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
                return 0
    #建立空的設定檔
    if event.message.text == '#create_config':
        if event.source.type == 'user':
            if _sql.select_config(uid) == []:
                content = _config.create_config(uid,user_name)
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            else:
                content = "%s 設定檔已存在" %user_name
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        if event.source.type == 'group':
            if _sql.select_config(gid) == []:
                content = _config.create_config(gid,'group')
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            else:
                content = "%s 設定檔已存在" %user_name
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    #刪除設定檔
    if re.match('^##del_config=(.+)',event.message.text):
        id = re.match('^##del_config=(.+)',event.message.text).group(1)
        print(id)
        if _sql.select_config(id) == []:
            content = "%s 設定檔不存在" % id 
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        else:
            content = _config.delete_config(id)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    #浮水印設定
    if re.match('^#浮水印%(.+)%f(\d+)%([t|e]\d)%(red|green|blue|white|black|pink|yellow|gold|#......)%al(\d+)%(p\d)',event.message.text):
        if event.source.type == 'user':    
            content = _config.add_watermark(uid,user_name,event.message.text)        
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        else:
            content = _sys_mg.m_addmark()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    #查浮水印怎麼使用
    if event.message.text in ['浮水印','浮水印功能','查浮水印','查浮水印怎麼用','浮水印怎麼使用','怎麼用浮水印','查浮水印用法']:
        content = _sys_mg.m_addmark()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0 
    #設定功能啟用
    if re.match('^#設定%(.+)=(on|off|開|關)',event.message.text):
        if re.match('^#設定%(.+)=(on|off|開|關)',event.message.text).group(1) !='小星星':
            content = '目前僅支援開關小星星對話功能'
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0
        if event.source.type == 'user':
            if _sql.select_config(uid) == []:
                content = _sys_mg.m_noconfig(user_name)
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            else:
                content = _config.function_config(uid,user_name,event.message.text)
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        if event.source.type == 'group':
            if _sql.select_config(uid) == []:
                content = _sys_mg.m_noconfig(user_name)
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            else:
                content = _config.function_config(gid,'group',event.message.text)
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))                  
        return 0
    #OS function print sys dir
    if re.match('^#oss=(.+)*',event.message.text):
        path = re.match('^#oss=(.+)*',event.message.text).group(1)
        content = str(os.listdir(path))
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    #imgur_function delete imgur album images imgur_album_images_delete
    if re.match('^#dimga=(.+)*',event.message.text):
        album = re.match('^#dimga=(.+)*',event.message.text).group(1)
        if album=='temp':
            album_id = 'sJMh0RE'
        content = _photos.imgur_album_images_delete(album_id)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    #imgur_images_delete
    if re.match('^dimg=(.+)',event.message.text):
        #print(event.message.text)
        img_id = re.match('^dimg=(.+)',event.message.text).group(1)
        #print(img_id)
        content = _photos.imgur_images_delete(img_id)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0 
    if re.match('^#adminhelp',event.message.text):
        content = _sys_mg.m_admin_function()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0       
    ####抽圖區####
    if event.message.text == '抽':
        image_message = _photos.random()
        print(image_message)
        line_bot_api.reply_message(event.reply_token, image_message)
        return 0
    if event.message.text in ['抽正妹','抽美女']:
        image_message = _photos.beauty_girls()
        line_bot_api.reply_message(event.reply_token, image_message)
        return 0
    if event.message.text in ['抽帥哥','抽鮮肉','抽猛男']:
        image_message = _photos.imgur_boys()
        line_bot_api.reply_message(event.reply_token, image_message)
        return 0
    if event.message.text in ["說笑話","講笑話","小星星說笑話","小星星講笑話"]:
        image_message = _photos.joke()
        line_bot_api.reply_message(event.reply_token, image_message)
        return 0
    if event.message.text in ["比大小"]:
        image_message = _photos.poker()
        line_bot_api.reply_message(event.reply_token, image_message)
        return 0 
    if event.message.text == '抽金句':
        image_message = _photos.gods_talk()
        line_bot_api.reply_message(event.reply_token, image_message)
        return 0 
    if event.message.text in ["現在吃什麼"]:
        image_message = _photos.food()
        line_bot_api.reply_message(event.reply_token, image_message)
        return 0
    if event.message.text == '抽單身':
        image_message = _photos.single()
        line_bot_api.reply_message(event.reply_token, image_message)
        return 0
    ####hsing####
    if event.message.text == "抽歡歌":
        content = _hsing.sing17()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0    
    if re.match('(.+)*歡歌(\d+)[:|=](.+)',event.message.text):
        match = re.match('(.+)*歡歌(\d+)[:|=](.+)',event.message.text)
        content = _hsing.s17uidsong(match.group(2),match.group(3))
        #content = s17uidsong(event.message.text)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        #gs_write('B11')
        return 0
    if re.match('^歡歌(\d+)',event.message.text):
        match = re.match('^歡歌(\d+)',event.message.text)
        content = _hsing.s17uidrandom(match.group(1))
        #content = s17uidrandom(event.message.text)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        #gs_write('B10')
        return 0
    #hsing and oksing link to mp3
    if re.search('(17sing|oksing)',event.message.text):
        res = event.message.text
        content = _hsing.tomp3(res)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0 
    #changba link to mp3
    if re.search('changba',event.message.text):
        res = event.message.text
        content = _hsing.changbamp3(res)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    #mojim search
    if re.search('^查歌詞=(.+)',event.message.text):
        res = re.search('^查歌詞=(.+)',event.message.text).group(1)
        content = _hsing.mojim(res)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    #查伴奏-伴唱聯盟
    if re.search('^查伴奏=(.+)',event.message.text):
        res = re.search('^查伴奏=(.+)',event.message.text).group(1)
        content = _hsing.songsearch17(res)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    ####占卜#####
    #查塔羅牌說明
    if re.search("查(塔羅牌|塔羅|tarot)說明(\d+)",event.message.text):
        tarot_content = _tarot.tarot_detail(int(re.search("查(塔羅牌|塔羅|tarot)說明(\d+)",event.message.text).group(2)))
        url = tarot_content[4]
        content = '{}\n\n{}\{}'.format(tarot_content[1],tarot_content[2],tarot_content[3])
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(
            event.reply_token, [image_message, TextSendMessage(text=content)])
        return 0
    #抽塔羅牌
    if re.match("^抽(塔羅牌|塔羅|tarot)(\d張)?",event.message.text):
        match = re.match("^抽(塔羅牌|塔羅|tarot)(\d張)?",event.message.text)
        if match.group(2) == None:
            tarot_content = _tarot.tarot_random()
            url = tarot_content[4]
            content = '{}\n\n{}\{}'.format(tarot_content[1],tarot_content[2],tarot_content[3])
            image_message = ImageSendMessage(
                original_content_url=url,
                preview_image_url=url
            )
            line_bot_api.reply_message(
                event.reply_token, [image_message, TextSendMessage(text=content)])
        elif match.group(2) == '3張':
            carousel_template_message = _tarot.traot_multicard_3()
            line_bot_api.reply_message(event.reply_token,carousel_template_message)
        elif match.group(2) == '5張':
            carousel_template_message = _tarot.traot_multicard_5()
            line_bot_api.reply_message(event.reply_token,carousel_template_message)
        return 0
    #每日星座
    if event.message.text in [ "牡羊座","金牛座","雙子座","巨蟹座","獅子座","處女座","天秤座","天蠍座","射手座","魔羯座","水瓶座","雙魚座"]:
        res = event.message.text
        content = _fate_ask.star(res)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        #gs_write('B13')
        return 0
    #媽祖靈籤
    if event.message.text == "抽籤":
        content = _fate_ask.ask()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        #gs_write('B8')
        return 0
    ####生活類####
    #查美食     
    if re.match('^(.+)*查美食=(\D.)[市縣]*(.+)*',event.message.text):
        match = re.match('^(.+)*查美食=(\D.)[市縣]*(.+)*',event.message.text)
        city = match.group(2).replace('新北','台北').replace('北市','台北')
        res = match.group(3)
        content = ifoodie_get(city,res)
        if re.match('^查詢位置暫無資料',str(content)):
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        else:
            carousel_template_message = content
            line_bot_api.reply_message(event.reply_token,carousel_template_message)
        #gs_write('B27')
        return 0
    #巴哈姆特
    if re.match('^巴哈=(.+)',event.message.text):
        res = re.match('^巴哈=(.+)',event.message.text).group(1)
        content = _life.gamer(res)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        #gs_write('B26')
        return 0
    #mygopen
    if re.match('^查證=(.+)',event.message.text):
        res = re.match('^查證=(.+)',event.message.text).group(1)
        content = _life.mygopen(res)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        #gs_write('B25')
        return 0
    #查地圖定位
    if re.match('(.+)*座標=(.+)',event.message.text): 
        match = re.match('(.+)*座標=(.+)',event.message.text)
        location = match.group(2)
        location_xy = _function.getGeoForAddress(location)
        if location_xy == "ZERO_RESULTS":
            content = random.choice(['這地點查不到哦','別一直亂玩啦','換個地方找看看','這到底是哪裡啊~','%玩我啊'%user_name])
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        else:
            location_message = LocationSendMessage(
            title='座標位置',
            address=location,
            latitude=location_xy[0],
            longitude=location_xy[1]
            )
            line_bot_api.reply_message(event.reply_token,location_message)
        #gs_write('B29')
        return 0
    ####氣象資訊####
    #更新觀測站資料
    if event.message.text == "#update_wp_state":
        _weather.wp_state_to_db()
        json_content = _weather.get_state_json()
        content = "update cominit"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    #查觀測站JSON檔
    if re.match('^#wp_state=(.+)',event.message.text):
        wp_state = re.match('^#wp_state=(.+)',event.message.text).group(1)
        json_content = _weather.get_state_json()    
        wp_json = json.loads(json_content[0][0])
        content = str(wp_json[wp_state])
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    #地點天氣update_wp_dict
    if re.match('(.+)*天氣=(.+)',event.message.text):
        match = re.match('(.+)*天氣=(.+)',event.message.text)
        loc = match.group(2)
        wp_content = _weather.getReportWithAPI(loc)
        content = '地點：{}\n{}'.format(loc,wp_content)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        #gs_write('B28')
        return 0
    #天氣預報
    if re.match('^查天氣(...)',event.message.text):
        location = re.match('^查天氣(...)',event.message.text).group(1).replace('台','臺')
        content = _weather.weather(location)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        #gs_write('B14')
        return 0
    #查颱風
    if re.match('^查颱風(.+)*',event.message.text):
        url = 'https://www.windy.com/?25.048,121.532,5'
        ty_content = _weather.ty()
        content = '{}\n颱風動態連結:{}\n------\n資料來源:中央氣象局&windy'.format(ty_content,url)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    #AQI
    if event.message.text == event.message.text in ["查PM2.5","查空氣品質","查pm2.5","AQI","現在空氣品質"]:
        res = _weather.AQI()
        url = res['link']
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(event.reply_token,image_message)
        #gs_write('B15')
        return 0      
    ####金融類####
    #匯率
    rate_list = "^美金|港幣|英鎊|澳幣|加拿大幣|加幣|新加坡幣|瑞士法郎|法郎|日圓|日幣|南非幣|瑞典幣|紐元|泰幣|泰銖|菲國比索|印尼幣|歐元|韓元|韓幣|越南盾|馬來幣|人民幣"
    if re.search(rate_list,event.message.text):
        if re.search("=",event.message.text):
            content = _fin.rate_ex(event.message.text)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            #gs_write('B22')
            return 0
        else:           
            rate_content = _fin.rate(re.search(rate_list,event.message.text).group(0)) 
            content = '臺灣銀行牌告匯率\n查詢時間:{}\n{} 1:{}\n\n走勢圖:{}'.format(rate_content[0],rate_content[1],rate_content[2],rate_content[4])
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            #gs_write('B23')
            return 0    
    ####遊戲區####
    #18啦遊戲
#    if re.match('18啦',event.message.text):        
#        content = _games.r18()
#        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
#        return 0
    if re.match('^18啦',event.message.text):
            content = _games.r18()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0 
    ####影音類####
    if re.match('^(聽歌|找到|youtube)=(.+)*',event.message.text):
        res = re.match('^(聽歌|找到|youtube)=(.+)*',event.message.text).group(2)
        content = _audio.youtube_search(res)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        #gs_write('B19')
        return 0
    ####小星星相關###
    if event.message.text in ['!help','功能表']:
        content = _sys_mg.m_function()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == '小星星粉絲頁':
        content = 'FB粉絲團連結：http://pcse.pw/83A5Q'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    #小星星福利社carousel_template_message
    if re.search("小星星(福利社|賣場|商店街)",event.message.text):
        carousel_template_message = _star_store.star_store()
        line_bot_api.reply_message(event.reply_token,carousel_template_message)
        #gs_write('B12')
        return 0
    words_list = "小星星|幹|操|fuck|三小|靠北|爆料|三字經|壞掉了|早安|早啊|晚安|睡囉|哈哈哈哈哈|(才|你|小星星)尿床|尿好了|有尿了"
    if re.search(words_list,event.message.text):
        key = '小星星'
        if event.source.type == 'group': 
            config = _sql.select_config(gid)
            if config != []:
                config_list = config[0]
                json_data = json.loads(config_list[2])
                if key in json_data['function_option']:
                    if json_data['function_option'][key] == 'on':
                        content = _star_talk.star_talk(event.message.text,user_name)
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
                    return 0
                else:
                    if re.search('小星星(怎麼|為什麼)不(會)?[回講說]話了',event.message.text):
                        content = random.choice(['%s 因為大家覺得我太吵，所以關掉了'%user_name,'%s 檢查一下設定吧'%user_name])
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
                    return 0
            else:
                content = _star_talk.star_talk(event.message.text,user_name)    
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
                return 0                  
        else:
            content = _star_talk.star_talk(event.message.text,user_name)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0            

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    
    print("event",event)
    
    if event.source.type == 'group':
        gid = event.source.group_id
        #print(gid)
        uid = event.source.user_id
        #print(uid)
        #profile = line_bot_api.get_group_member_profile(gid,uid)
        profile = _lineapi.get_group_member_profile(gid,uid)
        #print(profile)
        user_name = profile['displayName']
    if event.source.type == 'user':
        uid = event.source.user_id
        profile = line_bot_api.get_profile(event.source.user_id)
        user_name = profile.display_name                
     
    if event.source.type == 'user':
        uid = event.source.user_id
        message_content = line_bot_api.get_message_content(event.message.id)
        res = _photos.add_watermark(uid,message_content)
        if res == 'none':
            content = _sys_mg.m_addmark()
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
        else:
            url = res['link']
            img_id = res['id']
            del_messages = '下載完圖檔後，請輸入下面指令刪除圖檔 \ndimg={}'.format(img_id)
            image_message = ImageSendMessage(
                original_content_url=url,
                preview_image_url=url
            )         
            line_bot_api.reply_message(event.reply_token, [image_message, TextSendMessage(text=del_messages)]) 
            #gs_write('B30')
        return 0
    else:
        content = _sys_mg.m_addmark()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))  
        return 0
    
                     
if __name__ == '__main__':
    app.run()
