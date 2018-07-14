# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 11:07:15 2018
@author: 宇星
"""

import re
#import random
import configparser
import json
#from bs4 import BeautifulSoup
from flask import Flask, request, abort
#from imgurpython import ImgurClient

import function.game_zone
_games = function.game_zone.game_zone()

import function.sql
_sql = function.sql.Sql()

import function.config_setting
_config = function.config_setting.config_setting()

import function.sys_messages
_sys_mg = function.sys_messages.sys_messages()

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
        MessageEvent, TextMessage, TextSendMessage,
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
    #print("event.message.text:", event.message.text)
    #content = event.message.text
    #line_bot_api.reply_message(event.reply_token,[TextSendMessage(text=str(event)),TextSendMessage(text=content)])
    #取得event
    if event.message.text == 'getevent':
        content = event.message.text
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(text=str(event)),TextSendMessage(text=content)])
        return 0
    #取得設定檔
    if event.message.text=='getconfig':
        uid = event.source.user_id
        profile = line_bot_api.get_profile(event.source.user_id)
        user_name = profile.display_name
        if len(_sql.select_config(uid)) == 0:
            content = _sys_mg.m_noconfig(user_name)
            #print(content)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        else:        
            config = _sql.select_config(uid)
            config_list = config[0]
            uid=config_list[0]
            user_name = config_list[1]
            json_data = config_list[2]
            #json_content = json.loads(json_data)
            #print(json_content['watermark'])
            #data = json.parse(json)
            content = json_data
            #print(content)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    #建立空的設定檔
    if event.message.text == '#create_config':
        if event.source.type == 'user':
            uid = event.source.user_id
            profile = line_bot_api.get_profile(event.source.user_id)
            user_name = profile.display_name
            if len(_sql.select_config(uid)) == 0:
                content = _config.create_config(uid,user_name)
                #print(content)
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            else:
                content = "%s 設定檔已存在" %user_name
                #print(content)
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    #刪除設定檔
    if re.match('^##del_config=(.+)',event.message.text):
        if event.source.type == 'user':
            uid = re.match('^##del_config=(.+)',event.message.text).group(1)
            if len(_sql.select_config(uid)) == 0:
                content = "no user_id"
                #print (content)
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            else:
                content = _config.delete_config(uid)
                #print(content)
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    #浮水印設定
    if re.match('^#浮水印%(.+)%f(\d+)%([t|e]\d)%(red|green|blue|white|black|pink|yellow|gold|#......)%al(\d+)%(p\d)',event.message.text):
        #if event['source']['type'] == 'user':
#            uid = event['source']['userId']
#            user_name = "victor_冷男"
        if event.source.type == 'user':
            uid = event.source.user_id
            profile = line_bot_api.get_profile(event.source.user_id)                       
            user_name = profile.display_name
           
            content = _config.add_watermark(uid,user_name,event.message.text)
            #print(content)
            #content = _function.set_watermark(uid,match.group(1),match.group(2),match.group(3),match.group(4),match.group(5),match.group(6))            
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        else:
            content = _sys_mg.m_addmark()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            #print(content)
        return 0
    #查浮水印怎麼使用
    if event.message.text in ['浮水印','浮水印功能','查浮水印','查浮水印怎麼用','浮水印怎麼使用','怎麼用浮水印','查浮水印用法']:
        content = _sys_mg.m_addmark()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    #設定功能啟用
    if re.match('^#功能%(.+)=(on|off|開|關)',event.message.text):
        if event.source.type == 'user':
            uid = event.source.user_id
            profile = line_bot_api.get_profile(event.source.user_id)
            user_name = profile.display_name
            if len(_sql.select_config(uid)) == 0:
                content = _sys_mg.m_noconfig(user_name)
                #print(content)
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            else:
                content = _config.function_config(uid,user_name,event.message.text)
                #print(content)
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    #18啦遊戲
#    if re.match('18啦',event.message.text):        
#        content = _games.r18()
#        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
#        return 0
    if re.match('18啦',event.message.text):
        if event.source.type == 'user':
            uid = event.source.user_id
#            profile = line_bot_api.get_profile(event.source.user_id)
#            user_name = profile.display_name
            _user_json = _sql.select_config(uid)[0][2]
            _json_data = json.loads(_user_json)
            if _json_data['function_option'].get('18啦') == 'off':
                function_name = '18啦'
                content = _sys_mg.m_function_off(function_name)
                #print(content)
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            else:
                content = _games.r18()
                #print(content)
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        else:
            content = _games.r18()
            #print(content)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
                   
        return 0    
                     
if __name__ == '__main__':
    app.run()
