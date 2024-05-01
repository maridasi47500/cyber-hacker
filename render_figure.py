import re
from fichier import Fichier
import os
from mydb import Mydb
import traceback
import sys
import datetime
from datetime import date
class RenderFigure():
    def __init__(self,program):
        self.session={"name":"","notice":"","mysession":False}
        self.mytemplate="./mypage/index.html"
        self.path=program.get_path()
        self.title=program.get_title()
        self.headingone=program.get_title()
        self.redirect=""
        self.body=""
        self.params={"current_user_email":None,"current_user_name":None}
    
    def set_redirect(self,x):
        self.redirect=x
    def get_redirect(self):
        return self.redirect
    def set_session(self,x):
        self.session=x
    def get_session(self):
        return self.session
    def set_param(self,x,y):
        self.params[x]=y
    def getparams(self,param):
        try:
            x=self.params[param]
        except:
            x=None
        return x
    def render_body(self):
        try:
          mystr=""
          loc={"db":Mydb(),"session": self.session,"render_collection": self.render_collection,"params":self.params,"getparams": self.getparams,"Fichier":Fichier,"date":date,"datetime":datetime}
          for n in self.params:
              loc[n]=self.params[n]
          for j in self.body.split("<%"):
            if j[0] == "=":
              j=j[1:]
              if "%>" not in j:
                  mystr+=j
                  continue
              k=j.split("%>")
              print("my session",self.session)

              if k[0]:
                #print(k[0])
                l=exec("myvalue="+k[0], globals(), loc)
                mystr+=str(loc["myvalue"]) if loc["myvalue"] is not None else ""
              if k[1]:
                mystr+=k[1]

            else:
              if "%>" not in j:
                  mystr+=j
                  continue
              k=j.split("%>")
              print("my session",self.session)
              #loc={"db":Mydb(),"session": self.session,"render_collection": self.render_collection,"params":self.params,"getparams": self.getparams,"Fichier":Fichier,"date":date}
              #print(k[0])
              l=exec(k[0], globals(), loc)
              if k[1]:
                mystr+=k[1]
          print("render body bon")
          #print(mystr)
          return mystr
        except Exception as e:
          print("render body mauvais")
          l="<div style='background:red;color:white;'>erreurici pour afficher <div class=\"codeerreur\" style=\"background:black;color:white;\">"+k[0]+"</div>"+traceback.format_exc()+"<br>"+str(e)+"</div>".replace("\r\n",'<br>')

          return l
    def render_collection(self, collection,partial,as_,mylocals={}):
        print("render collection")
        try:
            myview=open(os.path.abspath("./"+partial),"r").read()
            mystr=""
            i=0
            k=[]
            paspremier=False
            ligne=0
            loc={"db":Mydb(),"paspremier":False,as_: "","index":"",  "params": self.params,"render_collection":self.render_collection,"date":date,"datetime":datetime}

            for x in collection:
                loc["index"]=i
                loc["paspremier"]=paspremier
                loc[as_]=x

                for j in myview.split("<%"):
                    ligne+=j.count("\r\n")
                    if len(j) > 0 and j[0] == "=":
                        j=j[1:]
                        if "%>" not in j:
                            mystr+=j
                            continue

                        k=j.split("%>")
                        #print(dict(x))
                        if k[0]:
                            #print(k[0], "content render")
                            #print(k[0])
                            l=exec("myvalue="+k[0], globals(), loc)
                            mystr+=str(loc["myvalue"])
                        if k[1]:
                            mystr+=k[1]
                    elif len(j) > 0:
                        if "%>" not in j:
                            mystr+=j
                            continue

                        k=j.split("%>")

                        #print(dict(x))
                        if k[0]:
                            #print(k[0], "content render")
                            #print(k[0])
                            l=exec(k[0], globals(), loc)
                            #mystr+=str(loc["myvalue"])
                        if k[1]:
                            mystr+=k[1]
                i+=1
                paspremier=True
            print("render collection bon")
            return mystr
        except Exception as e:
            print("render collection mauvais")
            raise ValueError("<meta charset=\"utf-8\"><div>Un certain truc sest mal passé avec<div style=\"background:black;color:#eb00eb;\" class=\"someerror\"> "+k[0]+"</div>---><div style=\"background:black;color:#eb00eb;\" class=\"someerror\">"+str(e)+"-- ligne "+str(ligne)+"</div></div>")
    def partie_de_mes_mots(self,balise="",text=""):
        r="<{balise}>{text}</{balise}>"
        s="""
        <html>
        <head>
        <title>{debutmots}</title>
        <h1>{mot}</h1>
        {plusdemots}
        </head>
        </html>
        """.format(debutmots=self.title, mot=self.headingone,plusdemots=self.body)
        return re.search(r, s)
    def debut_de_mes_mots(self,balise="div",text=""):
        r="<{balise}>{text}</{balise}>"
        s="""
        <html>
        <head>
        <title>{debutmots}</title>
        <h1>{mot}</h1>
        {plusdemots}
        </head>
        </html>
        """.format(debutmots=self.title, mot=self.headingone,plusdemots=self.body)
        return re.match(r, s)
    def fin_de_mes_mots(self,balise="div",text=""):
        r="<{balise}>{text}</{balise}>$"
        s="""
        <html>
        <head>
        <title>{debutmots}</title>
        <h1>{mot}</h1>
        {plusdemots}
        </head>
        </html>
        """.format(mot=self.headingone,plusdemots=self.body)
        return re.search(r, s)
    def ajouter_a_mes_mots(self,balise,text):
        r="<{balise}>{text}</{balise}>".format(balise=balise,text=text)
        self.body+=r

    def render_redirect(self):
        self.body="<a href=\"{url}\">{text}</a>".format(url=self.get_redirect(),text="la page a été redirigée")
        
        return self.body
    def set_json(self,x):
        self.json=True
        self.body=(x).encode("utf-8")
    def render_my_json(self,filename):

        self.body=filename
        self.body=self.render_body()
        try:
          return self.body.encode("utf-8")
        except:
          return self.body

    def render_some_json(self,filename):

        self.body=open(os.path.abspath(self.path+"/"+filename),"r").read()
        self.body=self.render_body()
        try:
          return self.body.encode("utf-8")
        except:
          return self.body

    def render_json(self):
        return self.body
    def render_only_figure(self,filename):
        self.body=open(os.path.abspath(self.path+"/"+filename),"r").read()
        self.body=self.render_body()
        try:
          return self.body.encode("utf-8")
        except:
          return self.body
    def render_figure(self,filename):
        try:
          self.body+=open(os.path.abspath(self.path+"/"+filename),"r").read()
          if self.mytemplate is not None:
              self.body= open(os.path.abspath(self.mytemplate),"r").read().format(debutmots=self.title, mot=self.headingone,plusdemot=self.body)
          self.body=self.render_body()
          while "<%" in self.body and "%>" in self.body:
            self.body=self.render_body()
          print("render figure bon")
          try:
            return self.body.encode("utf-8")
          except:
            return self.body
        except Exception as e:
          print("render figure mauvaos")
          return ("<meta charset=\"utf-8\"><div>Un certain truc sest mal passé avec<div style=\"background:black;color:#eb00eb;\" class=\"someerror\"> "+k[0]+"</div>---><div style=\"background:black;color:#eb00eb;\" class=\"someerror\">"+str(e)+"-- ligne "+str(ligne)+"</div></div>").encode("utf-8")
