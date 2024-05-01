# coding=utf-8
import sqlite3
import sys
from urllib.request import urlopen
import re as r
from textblob import TextBlob
from langdetect import DetectorFactory
from langdetect import detect
from google_trans_new import google_translator  



import re
from model import Model
class Video(Model):
    def __init__(self):
        DetectorFactory.seed = 0
        self.con=sqlite3.connect(self.mydb)
        self.con.row_factory = sqlite3.Row
        self.cur=self.con.cursor()
        self.cur.execute("""create table if not exists video(
        id integer primary key autoincrement,
        user_id text,
            title text,
            polarity text,
            description text,
            ip text,
            filename text
                    );""")
        self.con.commit()
        #self.con.close()
    def detect_and_translate(text,target_lang):
        result_lang = detect(text)
        if result_lang == target_lang:
          return text 
        else:
          translator = google_translator()
          translate_text = translator.translate(text,lang_src=result_lang,lang_tgt=target_lang)
          return translate_text 
    def getall(self):
        self.cur.execute("select video.*,user.username from video left join user on user.id = video.user_id order by video.id desc limit 5")

        row=self.cur.fetchall()
        return row
    def whatismyip(self):
        d = str(urlopen('http://checkip.dyndns.com/').read())
        return r.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(d).group(1)
    def whatismypolarity(self,text):
        blob = TextBlob(self.detect_and_translate(text,target_lang="en"))
        sentiment = blob.sentiment.polarity
        return sentiment
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
        myhash["ip"]=self.whatismyip()
        myhash["polarity"]=self.whatismypolarity(myhash["description"])
        try:
          self.cur.execute("insert into video (polarity,ip,user_id,title,description,filename) values (:polarity,:ip,:user_id,:title,:description,:filename)",myhash)
          self.con.commit()
          myid=str(self.cur.lastrowid)
        except Exception as e:
          print("my error"+str(e))
        azerty={}
        azerty["video_id"]=myid
        azerty["notice"]="votre video a été ajouté"
        return azerty




