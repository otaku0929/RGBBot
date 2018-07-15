# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 13:03:45 2018

@author: 宇星
"""

def main():
    
    _sys_mg=sys_messages()
    print(_sys_mg.m_addmark())
    
class sys_messages(object):
    
    def __init__ (self):
        self.obj_name = 'sys_messages'
    
    def m_function_off(self,function_name):
        return '此功能已被停用若要開啟請輸了：\n #功能%{}=on'.format(function_name)
        
    def m_noconfig(self,user_name):
        return '沒有 %s 的設定檔，請先輸入:\n #create_config \n建立設定檔' % (user_name)
    
    def m_addmark(self):
        return '此功能不能在群組使用\n\n\
請先設定浮水印輸出格式，方式如下:\n\n\
#浮水印%text%fn%ttf%color%al%pn\n\
例如 #浮水印%小星星浮水印%f72%t3%red%aln255%p9\n\
 ------------\n\
 *text:浮水印內容\n\
 *fn=字體大小\n\
 *ttf=字型：目前共有中文7,英文4種t1~t7 e1~e4 \n\
 *color=顏色:支援red|green|blue|white|break|pink|yellow|gold, 也可以輸入色票#ffffff\n\
 *aln=透明度:0~255 (建議不要小於128)\n\
 *pn=浮水印位置：以九宮格方式劃分'
 
    def m_function(self):
        helplist=['..!help',
                  '小星星指令集',
                  '',
                  '==抽圖類==',
                  '',
                  '..抽',
                  '..抽正妹',
                  '..抽鮮肉',
                  '..抽金句',
                  '..現在吃什麼',
                  '..講笑話',
                  '',
                  '===占卜類==',
                  '',           
                  '..抽塔羅牌/抽tarot',
                  '..塔羅牌3張/抽tarot3張',
                  '..抽塔羅牌5張/抽tarot5張', 
                  '..抽籤', 
                  '..星座名　ex天秤座',
                  '',
                  '==生活類==',
                  '',
                  '..巴哈+關鍵字  (查攻略',
                  '..查證+關鍵字  (查假消息',
                  '..查天氣縣市 ex查天氣台北市',
                  '..查天氣=地址 (查天氣松山機場',
                  '..查空氣品質',
                  '..天氣特報',
                  '..查颱風',
                  '..time (查農民曆)',
                  '..time20180101',
                  '..time2017010113',   
                  '..蘋果新聞',
                  '..看電影',
                  '..看電影+電影名',
                  '..本週上映',
                  '..查集點',
                  '..查咖啡',
                  '..PTTHOT',
                  '..PTT笨版',
                  '..PTT表特',
                  '..即時廢文',
                  '..傳送LINE座標',
                  '    (查座查附近的餐廳',
                  '',
                  '==金融類==',
                  '',
                  '..輸入美金、日幣可查匯率',
                  '..1000=美金 (查TWD換匯',
                  '..美金=100 (查美金換TWD',
                  '..查股市',
                  '..查股票股號 ex查股號鴻海',
                  '',
                  '==音樂類==',
                  '',
                  '..聽歌+關鍵字',
                  '   (查youtube影片',
                  '..youtube熱門',
                  '..youtube華語',
                  '..聽歌華語',
                  '..聽歌台語',
                  '..查歌詞+關鍵字',
                  '',
                  '==小遊戲==',
                  '',
                  '..18啦',
                  '..拉霸',
                  '',
                  '==歡歌類==',
                  '',
                  '..抽歡歌',
                  '..歡歌UID',
                  '..歡歌UID:關鍵字',
                  '..查伴奏+關鍵字',
                  '',
                  '== 小星星福利社 ==',
                  '',
                  '..小星星福利社 ',
                  '    (精選商品',
                  ''
                  '== 圖片功能類 ==',
                  '',
                  '..傳送圖片自動加浮水印',
                  '',
                  '== 小星星粉專 ==',
                  '',
                  ' http://pcse.pw/83A5Q '
                  ]
        content = ""
        for i in helplist:
            a = '{}\n'.format(i)
            content += a
           
        return content            
    
if __name__ == '__main__':
    main()