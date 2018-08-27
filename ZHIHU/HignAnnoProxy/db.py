#-*- coding:UTF-8 -*-
#数据库模块
#Author: 苍冥 e0t3rx

import sqlite3


class Database:
    def __init__(self, DB_NAME = "ProxyPoolDB.db", LOCATION = ""):
        try:
            #Create DB Cursor
            if LOCATION != "":
               DB_NAME = LOCATION + "/" + DB_NAME
            self.cursor = sqlite3.connect(DB_NAME, isolation_level=None).cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS TB_ProxyPool(ip TEXT, port INTEGER, protocol TEXT)")
        except sqlite3.OperationalError as e:
            #数据库繁忙，同时写入会发生错误
            #print("Error: Database Busy")
            pass

    def add(self, ip, port, protocol):
        try:
            self.cursor.execute("INSERT INTO TB_ProxyPool(ip, port, protocol) SELECT ?,?,? WHERE NOT EXISTS (SELECT * FROM TB_ProxyPool WHERE TB_ProxyPool.ip=? AND TB_ProxyPool.port=? AND TB_ProxyPool.protocol=?)", [ip,port,protocol,ip,port,protocol])
        except sqlite3.OperationalError as e:
            #数据库繁忙，同时写入会发生错误
            #print("Error: Database Busy")
            pass

    def modify(self):
        #后期更新再开发此功能
        pass

    def delete(self, ip, port, protocol):
        try:
            self.cursor.execute("DELETE FROM TB_ProxyPool WHERE ip=? AND port=? AND protocol=?",(ip, port, protocol))
        except sqlite3.OperationalError as e:
            #数据库繁忙，同时写入会发生错误
            #print("Error: Database Busy")
            pass


    #Sub-functions
    def fetch_all(self):
        try:
            #Returns a list of tuple objects, each stands for a proxy record
            return self.cursor.execute("SELECT * FROM TB_ProxyPool").fetchall()
        except sqlite3.OperationalError as e:
            #数据库繁忙，同时写入会发生错误
            #print("Error: Database Busy")
            pass

    def get_proxy_addr(self):
        aProxy = Database.fetch_all(self)
        aProxyAddr = []
        for Proxy in aProxy:
            ProxyAddress = str(Proxy[2])  + "://" + str(Proxy[0]) + ":" + str(Proxy[1])
            aProxyAddr.append(ProxyAddress)
        return  aProxyAddr

    def fetch_one(self,protocol):
        try:
            #Returns a list of tuple objects, each stands for a proxy record
            a = self.cursor.execute("SELECT * FROM TB_ProxyPool WHERE protocol=?", (protocol,)).fetchone()
            proxy = protocol + "://" + str(a[0]) + ":" + str(a[1])
            return proxy
        except sqlite3.OperationalError as e:
            #数据库繁忙，同时写入会发生错误
            #print("Error: Database Busy")
            pass
# # '''
# db = Database()
#
# a = db.fetch_all()
# for i in a:
# 	print(i[0])
# 	print(i[1])
# 	print(i[2])

# a = db.fetch_one("http")
# print(a)

# a = db.get_proxy_addr()
# for i in a:
#     print(i)