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


def pattern_mega(text):
    patterns = [
        'mega', 'mg', 'mu', 'ＭＥＧＡ', 'ＭＥ', 'ＭＵ',
        'ｍｅ', 'ｍｕ', 'ｍｅｇａ', 'GD', 'MG', 'google',
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True

def rate(res):

    url = "http://rate.bot.com.tw/xrt?Lang=zh-TW"
    dfs = pandas.read_html(url)
    currency = dfs[0]
    currency = currency.ix[:,0:3]
    currency.columns = [u'貨幣',u'匯率(賣)',u'匯率(買)']
    currency[u'貨幣'] = currency[u'貨幣'].str.split('\(',1).str[0]
    currency[u'貨幣'] = currency[u'貨幣'].str.split().str[0]
    #a = currency.values

    title = ""
    content = ""

    request = requests.get(url)
    soup = BeautifulSoup(request.content, "html.parser")

    datelist = soup.select('p.text-info')

    for data in datelist:
        ratedate = data.get_text().strip() 
 
    for a in currency.index:
        data = currency.ix[a,0]
        if data == res:
            title = currency.ix[a,0]
            rate =currency.ix[a,2]
            ratedata = '{} 1:{}'.format(title,rate)
          
    content = '臺灣銀行牌告匯率\n{}\n\n{}'.format(ratedate,ratedata)

    return content
     

def ratecount(res,nt,xt):
    
    url = "http://rate.bot.com.tw/xrt?Lang=zh-TW"
    dfs = pandas.read_html(url)
    currency = dfs[0]
    currency = currency.ix[:,0:3]
    currency.columns = [u'貨幣',u'匯率(賣)',u'匯率(買)']
    currency[u'貨幣'] = currency[u'貨幣'].str.split('\(',1).str[0]
    currency[u'貨幣'] = currency[u'貨幣'].str.split().str[0]

    a = currency.values

    for a in currency.index:
        data = currency.ix[a,0]
        if data == res:
            title = currency.ix[a,0]
            rate =currency.ix[a,2]
            ratecountnt = round(int(nt)/float(rate),2)
            ratecountxt = round(int(xt)*float(rate))
            if int(nt)>1 and int(xt)==1:
                content = '臺灣銀行牌告匯率 {} 1:{}\n台幣 {} 可換得 {} {}'.format(title,rate,nt,ratecountnt,title)
                return content
            if int(nt)==1 and int(xt)>1:
                content = '臺灣銀行牌告匯率 {} 1:{}\n兌換 {} {} 需要 {} 台幣'.format(title,rate,xt,title,ratecountxt)
            else:
                content = "輸入金額有誤 NT換 幣名n10000x1  換回NT 幣名n1x10000"

    return content


def weather(location):
    
    doc_name = "F-C0032-001"
    user_key = "CWB-A01FD046-AA6B-4C27-A307-616C33DB89B7"
    api_link = "http://opendata.cwb.gov.tw/opendataapi?dataid=%s&authorizationkey=%s" % (doc_name,user_key)
   
    headers = {'Authorization': user_key}
    res = requests.get("http://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?locationName=%s" % location,headers=headers)
    weather_api= res.json()

    weather_elements = weather_api['records']['location'][0]['weatherElement']

    Wx = (weather_elements[0]['time'])[0]['parameter'].get('parameterName')
    PoP = (weather_elements[1]['time'])[0]['parameter'].get('parameterName')
    MinT = (weather_elements[2]['time'])[0]['parameter'].get('parameterName')
    MaxT = (weather_elements[4]['time'])[0]['parameter'].get('parameterName')

    content = '{}\n天氣:{}\n溫度:{}C~{}C\n降雨機率:{}%'.format(location,Wx,MinT,MaxT,PoP)
    
    return content

def sweather():

    res = requests.get("http://opendata.cwb.gov.tw/api/v1/rest/datastore/W-C0033-002?Authorization=CWB-A01FD046-AA6B-4C27-A307-616C33DB89B7")
    weather_api= res.json()

    content=""
    weather_info = weather_api['records']['record'][0]['datasetInfo']['datasetDescription']
    weather_data = weather_api['records']['record'][0]['contents']['content']['contentText'].strip()

    content='<{}>\n{}'.format(weather_info,weather_data)
       
    return content


def pm25():

    url = 'http://opendata.epa.gov.tw/ws/Data/AQI/?$format=json'
    res=requests.get(url)
    soup = res.json()
    
    data = ""
    content=""

    for i in range(0,len(soup)-1):
        if soup[i].get('Status') in ['對敏感族群不健康','對所有族群不健康','非常不健康','危害']:
            County = soup[i].get('County')
            SiteName = soup[i].get('SiteName')
            AQI = soup[i].get('AQI')
            PM25 = soup[i].get('PM2.5')
            Status = soup[i].get('Status')
            data='城市:{}\n觀測站:{}\nAQI:{}\nPM2.5:{}\n空氣品質:{}\n\n'.format(County,SiteName,AQI,PM25,Status)
            content +=data
        else:
            pass
    return content

def ty():

    src = 'http://www.cwb.gov.tw/V7/prevent/typhoon/Data/PTA_NEW/index.htm?dumm=Wed#'
    url = urllib.request.urlopen(src)
    soup = BeautifulSoup(url, 'html.parser')
    data = soup.select('div.patch')
    text = data[0].get_text().strip()
    imgsoure = soup.select('div.download a')

    imgurl = imgsoure[0].get('href')
    imglink = 'http://www.cwb.gov.tw/V7/prevent/typhoon/Data/PTA_NEW/{}'.format(imgurl)

    content = '{}\n{}'.format(text,imglink)

    return content

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

def fwords(resf):
    words = resf
    wlist = (["美金","港幣","英鎊","澳幣","加拿大幣","新加坡幣","瑞士法郎","日圓","日幣","南非幣","瑞典幣","紐元","泰幣","菲國比索","印尼幣","歐元","韓元","越南盾","馬來幣","人民幣"])

    if words.find('n')>=2:
        res = words[0:words.find('n')].replace('日幣','日圓')
        nt = words[words.find('n')+1:words.find('x')]
        xt = words[words.find('x')+1:]
        content = ratecount(res,nt,xt)
        return content
    elif len(words) >=2:
        for data in wlist:
            if words[words.find(data,0):words.find(data,0)+len(data)] in wlist:
                m2list = words[words.find(data,0):words.find(data,0)+len(data)]
                messages_talk = m2list
                content = talk_messages(messages_talk)
                return content    
    
def talk_messages(messages_talk):

    if messages_talk in [ "美金","港幣","英鎊","澳幣","加拿大幣","新加坡幣","瑞士法郎","日圓","日幣","南非幣","瑞典幣","紐元","泰幣","菲國比索","印尼幣","歐元","韓元","越南盾","馬來幣","人民幣"]:
        res = messages_talk.replace('日幣','日圓')
        content = rate(res)
        return content


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event",event)
    print("event.groupID:",event.source)
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)

    grouplist = str(event.source)
    mlist = event.message.text
    words = event.message.text

    if event.message.text == "抽金句":
        client = ImgurClient('33ed33e765afedc', '04f0d5531b1d0978ff97fd990554c899e9e7e1f5')
        images = client.get_album_images('6FM69')
        index = random.randint(0, len(images) - 1)
        url = images[index].link
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(
            event.reply_token, image_message)
        return 0
    if event.message.text in ["說笑話","講笑話","小星星說笑話","小星星講笑話"]:
        client = ImgurClient('33ed33e765afedc', '04f0d5531b1d0978ff97fd990554c899e9e7e1f5')
        images = client.get_album_images('XpG2g')
        index = random.randint(0, len(images) - 1)
        url = images[index].link
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(
            event.reply_token, image_message)
        return 0
    if event.message.text in ["查PM2.5","查空氣品質","查pm2.5"]:
        content = pm25()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "天氣特報":
        content = sweather()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "查攝影比賽":
        content = photorace()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "checkid":
        content = getid(profile)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == 'Getid':
        if isinstance(event.source, SourceUser):
            profile = line_bot_api.get_profile(event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text='Display name: ' + profile.display_name
                    ),
                    TextSendMessage(
                        text='User_Id: ' + profile.user_id
                    )
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextMessage(text="Bot can't use profile API without user ID"))
    if event.message.text == 'Getgid':
        content = grouplist
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text=='查颱風':
        res = event.message.text
        content = ty()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
     if event.message.text=='攝影比賽查詢':
        res = event.message.text
        content = ty()
        line_bot_api.push_message(
            'Cd6ccb6c9e391a4cd613384154fec7330',
            TextSendMessage(text=content))
        return 0    
    if mlist[mlist.find('查天氣',0):3]=='查天氣':
        location = mlist[mlist.find('查天氣',0)+3:6].replace('台','臺')
        content = weather(location)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if len(words)>=1:
        resf = words
        content = fwords(resf)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0    

       
if __name__ == '__main__':
    app.run()

