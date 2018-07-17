# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 20:40:17 2018

@author: 宇星
"""
import random
from linebot.models import *

def main():
    print('OK')
#    store_content = star_store()
#    print(store_content)
    #print(store_content[0]['title'])
    
class star_store():
    def __init__(self):
        self.class_name = 'star_store'
        
    def star_store(self):
        
        store_content = self.get_star_store()
        
        carousel_template_message = TemplateSendMessage(
            alt_text='star_store_info',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url=store_content[0]['image'],
                        title=store_content[0]['title'],
                        text=store_content[0]['detail'],
                        actions=[
                            URITemplateAction(
                                label='詳細說明',
                                uri= store_content[0]['url']
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=store_content[1]['image'],
                        title=store_content[1]['title'],
                        text=store_content[1]['detail'],
                        actions=[
                            URITemplateAction(
                                label='詳細說明',
                                uri= store_content[1]['url']
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=store_content[2]['image'],
                        title=store_content[2]['title'],
                        text=store_content[2]['detail'],
                        actions=[
                            URITemplateAction(
                                label='詳細說明',
                                uri= store_content[2]['url']
                            )
                        ]
                    ),
                      CarouselColumn(
                        thumbnail_image_url=store_content[3]['image'],
                        title=store_content[3]['title'],
                        text=store_content[3]['detail'],
                        actions=[
                            URITemplateAction(
                                label='詳細說明',
                                uri= store_content[3]['url']
                            )
                        ]
                    ),
                       CarouselColumn(
                        thumbnail_image_url=store_content[4]['image'],
                        title=store_content[4]['title'],
                        text=store_content[4]['detail'],
                        actions=[
                            URITemplateAction(
                                label='詳細說明',
                                uri= store_content[4]['url']
                            )
                        ]
                    )
                ]
            )
        )
        
        return carousel_template_message
        
    def get_star_store(self):
        content_list = self.store_list()
        content_list.append(self.adv_list())
        random.shuffle(content_list)
        return content_list
    
        
    def store_list(self):
        dict=[
                {
                    'title':'夜光卡通造型汽車臨時停車卡',
                    'url':'https://seller.pcstore.com.tw/S198614447/C1200056412.htm',
                    'image':'https://i.imgur.com/jrg2cmw.jpg',
                    'detail':'環保硅膠材質，柔軟可見，不易變形\n尺寸：長21cm高9cm\n數字碼：0-9數字5排'
                        },
                {
                    'title':'長效防蚊扣',
                    'url':'https://seller.pcstore.com.tw/S198614447/C1200281208.htm',
                    'image':'https://i.imgur.com/8JxptEF.jpg',
                    'detail':'使用時效長，拆封使用就能有效驅趕蚊蟲時效長達2-3個月～',
                        },
                {
                    'title':'DIY迷你冰球圓形製冰球4入',
                    'url':'http://seller.pcstore.com.tw/S198614447/C1201104944.htm',
                    'image':'https://i.imgur.com/bTNaZLM.jpg',
                    'detail':'超級難融化，超級持久的大冰球，炎炎夏日有了它就不怕了。',
                        },
                 {
                    'title':'炫彩封口夾6入',
                    'url':'http://seller.pcstore.com.tw/S198614447/C1201902776.htm',
                    'image':'https://i.imgur.com/hPe1hnv.jpg',
                    'detail':'炫彩保鮮封夾、加長、加寬、封口平整、漂亮還很好打',
                        },
                 {
                    'title':'糖果色細長密封夾5入',
                    'url':'http://seller.pcstore.com.tw/S198614447/C1201906373.htm',
                    'image':'https://i.imgur.com/RrK6A9z.jpg',
                    'detail':'各種塑料袋已開過的食品袋，密封保存時使用！',
                        }      
                        
                ]
        
        random.shuffle(dict)
        return dict[0:4]
    
    
    def adv_list(self):
        dict=[
                {
                    'title':'匠師的故鄉美景農場',
                    'url':'https://beauty-farm.webnode.tw/',
                    'image':'https://i.imgur.com/ISbRAsA.jpg',
                    'detail':'匠師的故鄉‧包子匠師‧濱海體驗‧台中旅遊',
                        }, 
                ]
        
        
        return random.choice(dict)

if __name__ == '__main__':
    main()

