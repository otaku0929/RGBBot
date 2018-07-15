# -*- coding: utf-8 -*-
import pandas
import datetime
import pytz
import re
from functools import reduce

def main():
    _ff = financial()
    message = '日幣'
    print(_ff.rate(message))
    
    #return 'ok'
#    rate_data = "美金|港幣|英鎊|澳幣|加拿大幣|加幣|新加坡幣|瑞士法郎|法郎|日圓|日幣|南非幣|瑞典幣|紐元|泰幣|泰銖|菲國比索|印尼幣|歐元|韓元|韓幣|越南盾|馬來幣|人民幣"
#    message = '韓幣=1000'
#    #message = '小星星10000=美金不知道多少'
#    if re.search(rate_data,message):
#        if re.search("=",message):
#            content = rate_ex(message)
#            print(content)
#        else:
#            #print (rate(re.search(rate_data,message).group(0)))
#            rate_content = rate(re.search(rate_data,message).group(0))#.replace('日幣','日圓').replace('加幣','加拿大幣').replace('泰銖','泰幣').replace('法郎','瑞士法郎'))
#            content = '臺灣銀行牌告匯率\n查詢時間:{}\n{} 1:{}\n\n走勢圖:{}'.format(rate_content[0],rate_content[1],rate_content[2],rate_content[4])
#            print(content)
##    else:
##        print(rate('美金'))

class financial(object):
    def __init__(self):
        self.class_name = 'financial'
        
    def rate(self,rate):
        rep = self.rate_re()
        res = reduce(lambda a, kv: a.replace(*kv), rep.items(),rate) 
        #res = res.replace('日幣','日圓').replace('加幣','加拿大幣').replace('泰銖','泰幣').replace('法郎','瑞士法郎').replace('韓幣','韓元')
        url = "http://rate.bot.com.tw/xrt?Lang=zh-TW"
        dfs = pandas.read_html(url)
        currency = dfs[0]
        currency = currency.ix[:,0:3]
        currency.columns = [u'貨幣',u'匯率(賣)',u'匯率(買)']
        currency[u'貨幣'] = currency[u'貨幣'].str.split('\(',1).str[0]
        currency[u'貨幣'] = currency[u'貨幣'].str.split().str[0]
    
        tw = pytz.timezone('Asia/Taipei')
        #us = pytz.timezone('US/Pacific')
        now = datetime.datetime.now(tw).strftime("%Y-%m-%d %H:%M")
    
        for a in currency.index:
            data = currency.ix[a,0]
            if data == res:
                title = currency.ix[a,0]
                rate =currency.ix[a,2]
                re_rate = currency.ix[a,1]
                rate_chart_url = 'http://www.taiwanrate.org/exchange_rate_chart.php?c={}'.format(self.rate_chart(title))
                return [now,title,rate, re_rate, rate_chart_url]
    
    def rate_ex(self,res):
        #print(res)
        rate_ex = "(.+)(美金|港幣|英鎊|澳幣|加拿大幣|加幣|新加坡幣|瑞士法郎|法郎|日圓|日幣|南非幣|瑞典幣|紐元|泰幣|泰銖|菲國比索|印尼幣|歐元|韓元|韓幣|越南盾|馬來幣|人民幣)=(\d+)(\D+)"
        rate_rex = "(\D+)(\d+)=(美金|港幣|英鎊|澳幣|加拿大幣|加幣|新加坡幣|瑞士法郎|法郎|日圓|日幣|南非幣|瑞典幣|紐元|泰幣|泰銖|菲國比索|印尼幣|歐元|韓元|韓幣|越南盾|馬來幣|人民幣)(.+)"
        rate_ex_0 = "(美金|港幣|英鎊|澳幣|加拿大幣|加幣|新加坡幣|瑞士法郎|法郎|日圓|日幣|南非幣|瑞典幣|紐元|泰幣|泰銖|菲國比索|印尼幣|歐元|韓元|韓幣|越南盾|馬來幣|人民幣)=(\d+)"
        rate_rex_0 = "(\d+)=(美金|港幣|英鎊|澳幣|加拿大幣|加幣|新加坡幣|瑞士法郎|法郎|日圓|日幣|南非幣|瑞典幣|紐元|泰幣|泰銖|菲國比索|印尼幣|歐元|韓元|韓幣|越南盾|馬來幣|人民幣)"
        if re.match(rate_ex,res):
            rate_type = re.search(rate_ex,res).group(2)
            rate_list = self.rate(rate_type)
            money = int(re.search(rate_ex,res).group(3))
            get_rate = float(rate_list[2])
            count = round((money*get_rate),2)
            content = '臺灣銀行匯率 1:{}\n換算 {} {} = {} TWD'.format(get_rate, money, rate_type,count)
            return content
        if re.match(rate_rex,res):
            rate_type = re.search(rate_rex,res).group(3)
            rate_list = self.rate(rate_type)
            money = int(re.search(rate_rex,res).group(2))
            get_rate = float(rate_list[3])
            count = round((money/get_rate),2)
            content = '臺灣銀行匯率 1:{}\n換算 {} TWD = {} {}'.format(get_rate, money,rate_type,count)
            return content
        if re.match(rate_ex_0,res):
            rate_type = re.search(rate_ex_0,res).group(1)
            rate_list = self.rate(rate_type)
            money = int(re.search(rate_ex_0,res).group(2))
            get_rate = float(rate_list[2])
            count = round((money*get_rate),2)
            content = '臺灣銀行匯率 1:{}\n換算 {} {} = {} TWD'.format(get_rate, money, rate_type, count)       
            return content
        if re.match(rate_rex_0,res):
            rate_type = re.search(rate_rex_0,res).group(2)
            rate_list = self.rate(rate_type)
            money = int(re.search(rate_rex_0,res).group(1))
            get_rate = float(rate_list[2])
            count = round((money/get_rate),2)
            content = '臺灣銀行匯率 1:{}\n換算 {} TWD = {} {}'.format(get_rate, money,rate_type,count)
            return content
 
    def rate_re(self):
        rate_dict = {'日幣':'日圓',
                '日元':'日圓',
                '加幣':'加拿大幣',
                '泰銖':'泰幣',
                '法郎':'瑞士法郎',
                '韓幣':'韓元',
                '韓圓':'韓元',
                '美元':'美金',
                '美圓':'美金',
                '比索':'菲國比索',
                '新幣':'新加坡幣'
                }
        return rate_dict
                
    def rate_chart(self,res):
        rate_dict ={'美金':'USD',
                    '港幣':'HKD',
                    '英鎊':'GBP',
                    '澳幣':'AUD',
                    '加拿大幣':'CAD',
                    '新加坡幣':'SGD',
                    '瑞土法郎':'CHF',
                    '日圓':'JPY',
                    '南非幣':'ZAR',
                    '瑞典幣':'SEK',
                    '紐元':'NZD',
                    '泰幣':'THB',
                    '菲國比索':'PHP',
                    '印尼幣':'IDR',
                    '歐元':'EUR',
                    '韓元':'KRW',
                    '越南盾':'VND',
                    '馬來幣':'MYR',
                    '人民幣':'CNY'
                    };
        return rate_dict[res]
        #return 'http://www.taiwanrate.org/exchange_rate_chart.php?c={}'.format(res)
    

if __name__ == '__main__':
    main()
    
    
