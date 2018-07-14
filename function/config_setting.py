# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 17:37:50 2018

@author: 宇星
"""

import re
import json
from functools import reduce
import function.sql
_sql = function.sql.Sql()


def main():
    _config = config_setting()
    _config.add_watermark()

class config_setting(object):
    def __init__(self):
        self.class_name = 'config_setting'
        
    def create_config(self,id,user_name):
        config = '{"function_option":"none","watermark":"none"}'
        command = "insert into user_config (user_id, user_name, config) values('%s','%s','%s')" % (id,user_name,config)
        return(_sql.run(command))
        
    def delete_config(self,id):
        command = "delete from user_config where user_id = '%s'" % id
        print(command)
        return(_sql.run(command))
    
    def add_watermark(self,id,user_name,message):
        match = re.match('^#浮水印%(.+)%f(\d+)%([t|e]\d)%(red|green|blue|white|black|pink|yellow|gold|#......)%al(\d+)%(p\d)',message)
        text = match.group(1)
        fontsize = match.group(2)
        ttf = match.group(3)
        color = match.group(4)
        alpha = match.group(5)
        position = match.group(6)
        
        #config = {"watermark":{"text":text,"fontsize":fontsize,"ttf":ttf, "color":color, "alpha":alpha, "position":position}}
        new_config = '{"watermark":{"text":"%s","fontsize":"%s","ttf":"%s", "color":"%s", "alpha":"%s", "position":"%s"}}' % (text,fontsize,ttf,color,alpha,position)
        new_json = json.loads(new_config)
        
        #撈出舊的config_json 並更新json data
        _user_json = _sql.select_config(id)[0][2]
        _json_data = json.loads(_user_json)
        _json_data['watermark'] = new_json['watermark']
        #return(_json_data)

        #寫入資料庫
        config = json.dumps(_json_data)
        command = "update user_config set user_name = '%s',config = '%s' where user_id = '%s'" % (user_name,config,id)
        return(_sql.run(command))
            
        #print(_sql.select_config(id))
        
    def function_config(self,id,user_name,message):
        match = re.match('^#功能%(.+)=(on|off|開|關)',message)
        rep = {'開':'on','關':'off'}
        function_name = match.group(1)
        option = reduce(lambda a, kv: a.replace(*kv), rep.items(), match.group(2))      
        new_config = '{"function_option":{"%s":"%s"}}'%(function_name,option)
        new_json = json.loads(new_config)
        #print(new_json['function_option'])
        
        #撈出舊的config_json 並更新json data
        _user_json = _sql.select_config(id)[0][2]
        #_user_dump = json.dumps(_user_json)
        _json_data = json.loads(_user_json)
        if _json_data['function_option'] != 'none':
            print( _json_data['function_option'].get(function_name))
            if _json_data['function_option'].get(function_name) == None:
                _json_data['function_option'].update(new_json['function_option'])
                config = json.dumps(_json_data)
            else:
                _json_data['function_option'] = new_json['function_option']
                #print(_json_data)
                config = json.dumps(_json_data)
        else:
            _json_data['function_option'] = new_json['function_option']
            config = json.dumps(_json_data)
            #print(config)
            
        command = "update user_config set user_name = '%s',config = '%s' where user_id = '%s'" % (user_name,config,id)
        return(_sql.run(command))  

if __name__ == '__main__':
    main()