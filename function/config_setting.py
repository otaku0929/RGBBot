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
    config = {'function_option': {'18啦': 'off', '比大小': 'off', '小星星': 'off', '查天氣': 'off'}, 'watermark': {'text': '小星星浮水印', 'fontsize': '72', 'ttf': 't3', 'color': 'red', 'alpha': '255', 'position': 'p9'}}
    print(_config.config_list_user(config))

class config_setting(object):
    def __init__(self):
        self.class_name = 'config_setting'
        
    def create_config(self,id,user_name):
        config = '{"profile":{},"function_option":{},"watermark":{}}'
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
        
        if _sql.run(command) == "commit":
            return '完成設定，可以開始使用浮水印功能了'
        else:
            return 'error'
            
        #print(_sql.select_config(id))
        
    def function_config(self,id,user_name,message):
        match = re.match('^#設定%(.+)=(on|off|開|關)',message)
        rep = {'開':'on','關':'off'}
        function_name = match.group(1)
        option = reduce(lambda a, kv: a.replace(*kv), rep.items(), match.group(2))      
        new_config = '{"function_option":{"%s":"%s"}}'%(function_name,option)
        new_json = json.loads(new_config)
        
        #撈出舊的config_json 並更新json data
        _config_json = _sql.select_config(id)[0][2]
        #_user_dump = json.dumps(_user_json)
        _json_data = json.loads(_config_json)
        
        if function_name in _json_data['function_option'].keys():
             _json_data['function_option'][function_name] = new_json['function_option'][function_name]
             config = json.dumps(_json_data)
        else:
             _json_data['function_option'].update(new_json['function_option'])
             config = json.dumps(_json_data)
 
        command = "update user_config set user_name = '%s',config = '%s' where user_id = '%s'" % (user_name,config,id)

           
        if _sql.run(command) == "commit":
            return '完成設定，%s功能已%s'%(function_name,option)
        else:
            return 'error'


    def config_list(self,res):
        
        print(res)
        
        content = "＝＝功能設定＝＝"
        line_content=""
        if res == {}:
            content = '%s\n%s'%(content,'目前無任何設定')  
        else:
            if 'function_option' in res.keys():
                for obj in res:
                    title = "%s---\n"%obj
                    for key in res[obj]:
                        #print (key)
                        line = "%s:%s"%(key,res[obj][key])
                        line_content ='%s\n%s'%(line_content,line)
                        #print(line_content)           
                    title_content = '%s%s\n'%(title,line_content)
                    line_content = ""
                    content = '%s\n%s'%(content,title_content)
            else:
                for obj in res:
                    line = "%s:%s"%(obj,res[obj])
                    line_content ='%s\n%s'%(line_content,line)    
                    content = '%s\n%s'%(content,line_content) 
                
        return content

#    def config_list_group(self,res):
#        
#        content = "＝＝功能設定＝＝"
#        line_content=""
#        for obj in res:
#            if obj == 'n':
#                line_content = 'None'
#                break
#            else:
#                line = "%s:%s"%(obj,res[obj])
#                if line_content == "":
#                    line_content = line
#                else:
#                    line_content ='%s\n%s'%(line_content,line)
#
#        return('%s\n%s'%(content,line_content))
        
            
if __name__ == '__main__':
    main()