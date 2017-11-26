import time
import requests
import re
import random
import configparser
import urllib.request
import pandas
import gspread
import schedule
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from imgurpython import ImgurClient

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

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



def autophotorace():

    url = 'http://www.uart.org.tw/uart/show/tourney/tourney106.html'
    request = requests.get(url)
    soup = BeautifulSoup(request.content,"html.parser")

    plist = soup.select('tr tr')[3:]
   
    content = ""  
    for i in range(len(plist)-1):
        res = plist[i]
        cdata = photoracedata(res)
        _content = '{}\n'.format(cdata)
        content += _content
    
    line_bot_api.push_message(
        #'Ud0414e339e9c242b19a2dd22dd1f6189',
        'Cd6ccb6c9e391a4cd613384154fec7330',
        TextSendMessage(text=content))
  
def photorace():

    url = 'http://www.uart.org.tw/uart/show/tourney/tourney106.html'
    request = requests.get(url)
    soup = BeautifulSoup(request.content,"html.parser")

    plist = soup.select('tr tr')[3:]
   
    content = ""  
    for i in range(len(plist)-1):
        res = plist[i]
        cdata = photoracedata(res)
        _content = '{}\n'.format(cdata)
        content += _content
    return(content)
    
def photoracedata(res):

    for data in [res]:
       title = ''.join(data.select('a')[0].text.split())
       link = data.select('a')[0]['href'].strip()
       date = data.select('td[align="center"]')[2].text.strip().replace(' ','')
       content = '{}\n屆止日:{}\nhttp://www.uart.org.tw/uart/show/tourney/{}'.format(title,date,link)
    return (content)

 

                     
if __name__ == '__main__':
    schedule.every().monday.at("12:00").do(autophotorace)
    while True:
        schedule.run_pending()
        time.sleep(1)
    
