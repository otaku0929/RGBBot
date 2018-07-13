# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 11:07:15 2018

@author: 宇星
"""

import re
import random
import configparser
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from imgurpython import ImgurClient

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
    #print("event",event)
    #print("event.groupID:",event.source)
    #print("event.reply_token:", event.reply_token)
    #print("event.message.text:", event.message.text)
    
    content = event.message.text
    line_bot_api.reply_message(event.reply_token,[TextSendMessage(text=str(event)),TextSendMessage(text=content)])
    return 0
                     
if __name__ == '__main__':
    app.run()
