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
    if event.message.text == 'getevent':
        content = event.message.text
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(text=str(event)),TextSendMessage(text=content)])
        return 0
    if event.message.text == 'getconfig':
        if event.source.type == 'user':
            uid = event.source.user_id
            config = _sql.select_config(uid)[0]
            content = config[2]
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
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
    if re.match('18啦',event.message.text):        
        content = _games.r18()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    
                     
if __name__ == '__main__':
    app.run()
