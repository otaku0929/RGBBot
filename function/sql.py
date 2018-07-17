# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 14:50:02 2018

@author: 宇星
"""

import psycopg2
import os
import urllib.parse as urlparse

def main():
    _sql = Sql()
    #command = "select * from user_config"
    id = 'C486996bc0cf57372409c1dc6d7a4f6f3'
    config = _sql.select_config(id)
    if config == []:
        print ('0')
    else:
        #print (config)
        print(_sql.delete_config(id))


class Sql(object):
        
         
    def __init__(self):
        
        #url = urlparse.urlparse(os.environ['DATABASE_URL'])
        url = urlparse.urlparse('postgres://emghycqpjwctwr:04a3e938a72371fd03f0ed0428836f805c95b08fc332e9976fa9f2f82cdc1549@ec2-54-83-33-213.compute-1.amazonaws.com:5432/dcfuue2glgrc2m')
        
        self.class_name = 'Sql'
        self.database = url.path[1:]
        self.user = url.username
        self.password = url.password
        self.host= url.hostname
        self.port= url.port
        #self.connstr = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
        
#    def __init__(self):
#        self.class_name = 'Sql'
#        self.database = 'twstar'
#        self.user = 'pyadmin'
#        self.password = 'pyadmin'
#        self.host='127.0.0.1'
#        self.port='5432'
#        self.connstr = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
#
    def run (self,command):
        
        #print(command)
        conn =psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
         
        cur=conn.cursor()
         
        cur.execute(command)
        conn.commit()
        
        conn.close()
 
        return 'commit'

    def select(self,command):
        
        conn =psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
         
        cur=conn.cursor()
         
        cur.execute(command)
        rows = cur.fetchall()
        
        conn.close()
 
        return rows       
        
        
   
    def select_config(self,id):
        
        sql_command = "select user_id, user_name, config from user_config where user_id ='%s'" % (id)
        
        conn =psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
         
        cur=conn.cursor()
         
        cur.execute(sql_command)
        rows = cur.fetchall()
        
        conn.close()
 
        return rows
         
    def insert_config(self,uid,name,config):

            command = "insert into user_config (user_id, user_name, config) values('%s','%s','%s')" % (uid,name,config)
            conn = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
            cur=conn.cursor()
            
            #command = "insert into user_config (user_id, user_name, config) values('{}','{}','{}')".format(uid,name,config)
            
            cur.execute(command);
    
            conn.commit()
            conn.close()
            
            return "insert ok"
        
#        
#        try:
#            command = "insert into user_config (user_id, user_name, config) values('%s','%s','%s')" % (uid,name,config)
#            conn = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
#            cur=conn.cursor()
#            
#            #command = "insert into user_config (user_id, user_name, config) values('{}','{}','{}')".format(uid,name,config)
#            
#            cur.execute(command);
#    
#            conn.commit()
#            conn.close()
#            
#            return "insert ok"
#            
#        except:
#            return 'insert error'
    
    def update_config(self,uid,name,config):
        
        
        command = "update user_config set user_name = '%s',config = '%s' where user_id = '%s'" % (name,config,uid)
        print(command)
        conn = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
        cur=conn.cursor()
        
        #command = "update user_config set user_name = '{}',config = '{}' where user_id = '{}'".format(name,config,uid)
        cur.execute(command);
        conn.commit()
        
        #row = self.select(uid)
        
        conn.close()
        
        return "update ok"
        
#        try:
#            print(config)
#            command = "update user_config set user_name = '%s',config = '%s' where user_id = '%s'" % (name,config,uid)
#            conn = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
#            cur=conn.cursor()
#            
#            #command = "update user_config set user_name = '{}',config = '{}' where user_id = '{}'".format(name,config,uid)
#            cur.execute(command);
#            conn.commit()
#            
#            #row = self.select(uid)
#            
#            conn.close()
#            
#            return "update ok"
#            
#        except:
#            return ('update error')
        
    def delete_config(self,id):
        
        conn = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
        cur=conn.cursor()
        
        command = "delete from user_config where user_id = '%s'"%id
        cur.execute(command);
        conn.commit()
        
        #row = self.select(uid)
        
        conn.close()
        
        return "%s Config deleted"%id
         

    def temp_insert_row(self):
        conn =psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
        
        cur = conn.cursor()

        cur.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (1, 'Paul', 32, 'California', 20000.00 )");    
        cur.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (2, 'Allen', 25, 'Texas', 15000.00 )");       
        cur.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )");        
        cur.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )");
        
        conn.commit()

        print ("Table created successfully" )       

        conn.close()

    def temp_create_table(self):
        
        conn =psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
        print ("Opened database successfully")
        
        cur = conn.cursor()
#        cur.execute('''CREATE TABLE user_config
#               (user_id varchar(50) PRIMARY KEY NOT NULL,
#               user_name TEXT,
#               config TEXT);''')
        cur.execute('''CREATE TABLE system_json
               (id varchar(4) PRIMARY KEY NOT NULL,
               json_name varchar(50),
               json_file TEXT);''')
        
        print ("Table created successfully")
        
        conn.commit()
        conn.close()
        

if __name__ == '__main__':
    main()
