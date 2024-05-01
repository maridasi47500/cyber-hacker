# coding=utf-8
import sqlite3
import sys
import re
from urllib.request import urlopen
import re as r
from langdetect import DetectorFactory
from langdetect import detect
from deep_translator import GoogleTranslator

from model import Model
from textblob import TextBlob
class Comment(Model):
    def __init__(self):
        self.con=sqlite3.connect(self.mydb)
        self.con.row_factory = sqlite3.Row
        self.cur=self.con.cursor()
        self.cur.execute("""create table if not exists comment(
        id integer primary key autoincrement,
        video_id text,
            polarity text,
            user_id text,
            content text,
            ip text
                    );""")
        self.con.commit()
        #self.con.close()
    def detect_and_translate(self,text,target_lang):
        result_lang = detect(text)
        print("langue détectée:"+result_lang)
        if result_lang == target_lang:
          return text 
        else:
          translator = GoogleTranslator(source=result_lang, target=target_lang)
          translate_text = translator.translate(text)
          return translate_text 
    def whatismyip(self):
        d = str(urlopen('http://checkip.dyndns.com/').read())
        return r.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(d).group(1)
    def whatismypolarity(self,text):
        blob = TextBlob(self.detect_and_translate(text,"en"))
        sentiment = blob.sentiment.polarity
        return sentiment
    def getallbyvideoid(self,videoid):
        self.cur.execute("select comment.*,user.username from comment left join user on user.id = comment.user_id where comment.video_id = ?",(videoid,))

        row=self.cur.fetchall()
        return row
    def deletebyid(self,myid):

        self.cur.execute("delete from comment where id = ?",(myid,))
        job=self.cur.fetchall()
        self.con.commit()
        return None
    def getbyid(self,myid):
        self.cur.execute("select * from comment where id = ?",(myid,))
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
        myhash["ip"]=self.whatismyip()
        myhash["polarity"]=self.whatismypolarity(myhash["content"])
        try:
          self.cur.execute("insert into comment (polarity,video_id,user_id,content,ip) values (:polarity,:video_id,:user_id,:content,:ip)",myhash)
          self.con.commit()
          myid=str(self.cur.lastrowid)
        except Exception as e:
          print("my error"+str(e))
        azerty={}
        azerty["comment_id"]=myid
        azerty["notice"]="votre comment a été ajouté"
        return azerty




