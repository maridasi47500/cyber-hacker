# coding=utf-8
import sqlite3
import sys
import re
from model import Model
class Video(Model):
    def __init__(self):
        self.con=sqlite3.connect(self.mydb)
        self.con.row_factory = sqlite3.Row
        self.cur=self.con.cursor()
        self.cur.execute("""create table if not exists video(
        id integer primary key autoincrement,
        user_id text,
            title text,
            description text,
            filename text
                    );""")
        self.con.commit()
        #self.con.close()
    def getall(self):
        self.cur.execute("select video.*,user.username from video left join user on user.id = video.user_id order by video.id desc limit 5")

        row=self.cur.fetchall()
        return row
    def deletebyid(self,myid):

        self.cur.execute("delete from video where id = ?",(myid,))
        job=self.cur.fetchall()
        self.con.commit()
        return None
    def getbyid(self,myid):
        self.cur.execute("select video.*, user.username from video left join user on user.id = video.user_id where video.id = ?",(myid,))
        row=dict(self.cur.fetchone())
        print(row["id"], "row id")
        job=self.cur.fetchall()
        return row
    def create(self,params):
        print("ok")
        myhash={}
        for x in params:
            if 'confirmation' in x:
                continue
            if 'envoyer' in x:
                continue
            if '[' not in x and x not in ['routeparams']:
                #print("my params",x,params[x])
                try:
                  myhash[x]=str(params[x].decode())
                except:
                  myhash[x]=str(params[x])
        print("M Y H A S H")
        print(myhash,myhash.keys())
        myid=None
        try:
          self.cur.execute("insert into video (user_id,title,description,filename) values (:user_id,:title,:description,:filename)",myhash)
          self.con.commit()
          myid=str(self.cur.lastrowid)
        except Exception as e:
          print("my error"+str(e))
        azerty={}
        azerty["video_id"]=myid
        azerty["notice"]="votre video a été ajouté"
        return azerty




