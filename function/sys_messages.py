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
    
    
if __name__ == '__main__':
    main()