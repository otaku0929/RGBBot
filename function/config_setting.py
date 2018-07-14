# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 17:37:50 2018

@author: 宇星
"""

import re

import function.sql
_sql = function.sql.Sql()


def main():
    _config = config_setting()
    _config.add_watermark()

class config_setting(object):
    def __init__(self):
        self.class_name = 'config_setting'
        
    def add_watermark(self,id,user_name,message):
        match = re.match('^#浮水印%(.+)%f(\d+)%([t|e]\d)%(red|green|blue|white|black|pink|yellow|gold|#......)%al(\d+)%(p\d)',message)
        text = match.group(1)
        fontsize = match.group(2)
        ttf = match.group(3)
        color = match.group(4)
        alpha = match.group(5)
        position = match.group(6)
        
        #config = {"watermark":{"text":text,"fontsize":fontsize,"ttf":ttf, "color":color, "alpha":alpha, "position":position}}
        config = '{"watermark":{"text":"%s","fontsize":"%s","ttf":"%s", "color":"%s", "alpha":"%s", "position":"%s"}}' % (text,fontsize,ttf,color,alpha,position)
        #config_exists = _sql.select(id)        
        #print(command)
        
        print(len(_sql.select_config(id)))
        if len(_sql.select_config(id)) == 0: 
            print('insert')
            command = "insert into user_config (user_id, user_name, config) values('%s','%s','%s')" % (id,user_name,config)
            #print(config)
            print(_sql.insert_config(id,user_name,config))
        else:
            print('update')
            command = "update user_config set user_name = '%s',config = '%s' where user_id = '%s'" % (user_name,config,id)
            print(_sql.run(command))
            
        print(_sql.select_config(id))
        
        #return(config)
    

if __name__ == '__main__':
    main()