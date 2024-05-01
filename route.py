from directory import Directory
from render_figure import RenderFigure
from user import User
from mydb import Mydb

from vid import Vid

from mypic import Pic
from javascript import Js
from stylesheet import Css
import re
import traceback
import sys

class Route():
    def __init__(self):
        self.dbUsers=User()
        self.Program=Directory("Youtube Upload your vids urself")
        self.Program.set_path("./")
        self.mysession={"notice":None,"email":None,"name":None}
        self.render_figure=RenderFigure(self.Program)
        self.db=Mydb()
        self.getparams=("id",)
    def set_post_data(self,x):
        self.post_data=x
    def get_some_post_data(self,params=()):
        x={}
        try:
          for y in params:
              print(self.post_data[y])
              x[y]=self.post_data[y][0]
        except:
          print("wow")
        return x
    def get_post_data(self):
        return self.post_data
    def set_my_session(self,x):
        print("set session",x)
        self.Program.set_my_session(x)
        self.render_figure.set_session(self.Program.get_session())
    def set_redirect(self,x):
        self.Program.set_redirect(x)
        self.render_figure.set_redirect(self.Program.get_redirect())
    def render_some_json(self,x):
        self.Program.set_json(True)
        return self.render_figure.render_some_json(x)
    def render_my_json(self,x):
        self.Program.set_json(True)
        return self.render_figure.render_my_json(x)
    def set_json(self,x):
        self.Program.set_json(x)
        self.render_figure.set_json(self.Program.get_json())
    def set_notice(self,x):
        print("set session",x)
        self.Program.set_session_params({"notice":x})
        self.render_figure.set_session(self.Program.get_session())
    def set_session(self,x):
        print("set session",x)
        self.Program.set_session(x)
        self.render_figure.set_session(self.Program.get_session())
    def get_this_get_param(self,x,params):
        print("set session",x)
        hey={}
        for a in x:
          hey[a]=params[a][0]
        return hey
    def get_this_route_param(self,x,params):
        print("set session",x)
        return dict(zip(x,params["routeparams"]))
    def logout(self,search):
        self.Program.logout()
        self.set_notice("vous êtes déconnecté(e)")
        self.set_redirect("/sign_in")

        return self.render_figure.render_redirect()
    def welcome(self,search):
        return self.render_figure.render_figure("welcome/index.html")
    def getenregistrement(self,search):
        return self.render_some_json("welcome/somerecording.json")
    def audio_save(self,search):
        myparam=self.get_post_data()(params=("recording",))
        hi=""
        return self.render_some_json("welcome/hey.json")
    def voirsearch(self,wow):

        myparam=self.get_some_post_data(params=("search",))
        print(myparam,"P A R A M E T R E")
        s=myparam["search"]
        try:
          self.set_notice("vous avez cherché "+s.encode())

        except:
          self.set_notice("erreur quand vous avez envoyé le formulaire")
        self.render_figure.set_param("search",s)
        return self.render_figure.render_figure("welcome/voirsearch.html")
    def createvideo(self,search):
        myparam=self.get_post_data()(params=("title","description","filename","user_id",))
        hi=self.db.Video.create(myparam)
        if hi:
          self.set_notice("votre vidéo a été uploadée à youtube")
          self.render_figure.set_param("video_id", hi["video_id"])
          return self.render_some_json("welcome/myvid.json")
        else:
          self.set_notice("erreur quand vous avez envoyé le formulaire")
          return self.render_some_json("welcome/mypic.json")
    def mydiv(self,search):
        myparam=self.get_some_post_data(params=("div1","user_id"))
        hi=self.db.Link.find_by_url(url=myparam["div1"],user_id=myparam["user_id"])
        self.render_figure.set_param("url",hi)
        return self.render_some_json("welcome/myurl.json")
    def myband(self,search):
        myparam=self.get_some_post_data(params=("div1",))
        print(myparam, "my band fync")
        hi=self.db.Member.getallbybandid(myparam["div1"])
        self.render_figure.set_param("members",hi)
        return self.render_some_json("welcome/myband.json")
    def myurl(self,search):
        myparam=self.get_post_data()(params=("url","shorturl","div","user_id","band_id","member_id"))
        hi=self.db.Link.create(myparam)
        if hi:
          self.set_notice("votre article a été téléchargé")
        else:
          self.set_notice("erreur quand vous avez envoyé le formulaire")
        self.render_figure.set_param("post_id",hi["post_id"])
        return self.render_some_json("welcome/mypost.json")
    def updatepost(self,search):
        myparam=self.get_post_data()(params=("id","title","content",))
        hi=self.db.Post.update(myparam)
        if hi:
          self.set_notice("votre post a été modifié")
        else:
          self.set_notice("erreur quand vous avez envoyé le formulaire")
        self.render_figure.set_param("post_id",myparam["id"])
        return self.render_some_json("welcome/mypost.json")
    def createpost(self,search):
        myparam=self.get_post_data()(params=("band_id","user_id","title","content",))
        hi=self.db.Post.create(myparam)
        if hi:
          self.set_notice("votre post a été ajouté")
        else:
          self.set_notice("erreur quand vous avez envoyé le formulaire")
        self.render_figure.set_param("post_id",hi["post_id"])
        return self.render_some_json("welcome/mypost.json")
    def createband(self,search):
        myparam=self.get_post_data()(params=("name",))
        hi=self.db.Band.create(myparam)
        if hi:
          self.set_notice("votre band a été ajouté")
        else:
          self.set_notice("erreur quand vous avez envoyé le formulaire")
        return self.render_some_json("welcome/mypic.json")
    def createmember(self,search):
        myparam=self.get_post_data()(params=("band_id","name",))
        hi=self.db.Member.create(myparam)
        if hi:
          self.set_notice("votre member a été ajouté")
        else:
          self.set_notice("erreur quand vous avez envoyé le formulaire")
        return self.render_some_json("welcome/mypic.json")
    def createaddress(self,search):
        myparam=self.get_post_data()(params=("user_id","name","email",))
        hi=self.db.Address.create(myparam)
        if hi:
          self.set_notice("votre address a été ajouté")
        else:
          self.set_notice("erreur quand vous avez envoyé le formulaire")
        return self.render_some_json("welcome/address.json")
    def sendemail(self,search):
        myparam=self.get_post_data()(params=("sent","from","to","object","content","envoyeremail"))
        hi=self.db.Message.create(myparam)
        if hi and hi["sent"] == "1":
          self.set_notice("votre email a été envoyé")
        elif hi:
          self.set_notice("votre email a mis dans les brouillons")
        else:
          self.set_notice("erreur quand vous avez envoyé le formulaire")
        return self.render_some_json("welcome/mypic.json")
    def new1(self,search):
        myparam=self.get_post_data()(params=("script","missiontarget_id","missiontype_id","missionprogram_id",))
        #hi=self.dbMissionscript.create(myparam)
        return self.render_some_json("welcome/mypic.json")
    def nouveauevent(self,search):
        myparam=self.get_post_data()(params=("date","heure","organization_id","place_id", "subtitle","recording","privpubl"))
        self.render_figure.set_param("redirect","/")
        x=None
        x="hey"
        if x:
          self.set_notice("votre évènement a été ajouté")
        else:
          self.set_code422(True)
          self.set_notice("erreur quand votre évènement a été ajouté")
        return self.render_some_json("welcome/redirect.json")
    def nouveaulieu(self,search):
        myparam=self.get_post_data()(params=("pic","name",))
        self.render_figure.set_param("redirect","/")
        x=""
        if x:
          self.set_notice("votre lieu a été ajouté")
        else:
          self.set_code422(True)
        return self.render_some_json("welcome/redirect.json")
    def nouveauhack(self,search):
        myparam=self.get_post_data()(params=("person_id","place_id","text",))
        self.render_figure.set_param("redirect","/")
        x=""
        if x:
          self.set_notice("votre hack a été ajouté")
        else:
          self.set_code422(True)
        return self.render_some_json("welcome/redirect.json")
    def nouvelenregistrement(self,search):
        myparam=self.get_post_data()(params=("event_id","language","recording",))
        self.render_figure.set_param("redirect","/")
        x=""
        if x:
          self.set_notice("votre enregistrement a été ajoutée")
        else:
          self.set_code422(True)
        return self.render_some_json("welcome/redirect.json")
    def nouvellerumeur(self,search):
        myparam=self.get_post_data()(params=("person_id","place_id","text",))
        self.render_figure.set_param("redirect","/")
        x=""
        if x:
          self.set_notice("votre rumeur a été ajoutée")
        else:
          self.set_code422(True)
        return self.render_some_json("welcome/redirect.json")
    def nouvellepersonne(self,search):
        myparam=self.get_post_data()(params=("name","pic",))
        self.render_figure.set_param("redirect","/")
        x=""
        if x:
          self.set_notice("votre personne a été ajoutée")
        else:
          self.set_code422(True)
        return self.render_some_json("welcome/redirect.json")
    def enregistrer(self,search):
        print("hello action")
        self.render_figure.set_param("enregistrer",True)
        return self.render_figure.render_figure("welcome/radio.html")
    def aboutme(self,search):
        print("hello action")
        print("hello action")
        print("hello action")
        return self.render_figure.render_figure("welcome/aboutme.html")
    def hello(self,search):
        print("hello action")
        self.render_figure.set_param("videos",self.db.Video.getall())
        return self.render_figure.render_figure("welcome/index.html")
    def delete_user(self,params={}):
        getparams=("id",)
        myparam=self.post_data(self.getparams)
        self.render_figure.set_param("user",User().deletebyid(myparam["id"]))
        self.set_redirect("/")
        return self.render_figure.render_redirect()
    def edit_user(self,params={}):
        getparams=("id",)

        myparam=self.get_this_route_param(getparams,params)
        print("route params")
        self.render_figure.set_param("user",User().getbyid(myparam["id"]))
        return self.render_figure.render_figure("user/edituser.html")
    def editerpost(self,params={}):
        getparams=("id",)
        print("get param, action see my new",getparams)
        myparam=self.get_this_route_param(getparams,params)
        self.render_figure.set_param("post",self.db.Post.getbyid(myparam["id"]))
        return self.render_figure.render_figure("ajouter/editerpost.html")
    def seevideo(self,params={}):
        getparams=("id",)
        print("get param, action see my new",getparams)
        myparam=self.get_this_route_param(getparams,params)
        self.render_figure.set_param("video",self.db.Video.getbyid(myparam["id"]))
        return self.render_figure.render_figure("ajouter/voirvideo.html")
    def voirpersonne(self,params={}):
        getparams=("id",)
        print("get param, action see my new",getparams)
        myparam=self.get_this_route_param(getparams,params)
        try:
          personn1=""
          self.render_figure.set_param("person",personn1)

          if not personn1:
            self.Program.set_code422(True);
            return self.render_some_json("ajouter/personne1.json")
          return self.render_some_json("ajouter/personne.json")
        except:
          self.Program.set_code422(True);
          return self.render_some_json("ajouter/personne1.json")
    def seeuser(self,params={}):
        getparams=("id",)
        print("get param, action see my new",getparams)
        myparam=self.get_this_route_param(getparams,params)
        return self.render_figure.set_param("user",User().getbyid(myparam["id"]))
    def myusers(self,params={}):
        self.render_figure.set_param("users",User().getall())
        return self.render_figure.render_figure("user/users.html")
    def update_user(self,params={}):
        myparam=self.post_data(self.getparams)
        self.user=self.dbUsers.update(params)
        self.set_session(self.user)
        self.set_redirect(("/seeuser/"+params["id"][0]))
    def login(self,s):
        search=self.get_post_data()(params=("phone","password"))
        self.user=self.dbUsers.getbyphonepw(search["phone"],search["password"])
        print("user trouve", self.user)
        if self.user["phone"] != "":
            print("redirect carte didentite")
            self.set_session(self.user)
            self.set_json("{\"redirect\":\"/\"}")
        else:
            self.set_json("{\"redirect\":\"/youbank\"}")
            print("session login",self.Program.get_session())
        return self.render_figure.render_json()
    def search(self,search): 
        return self.render_figure.render_figure("ajouter/search.html")
    def addvideo(self,search): 
        return self.render_figure.render_figure("ajouter/video.html")
    def addmember(self,search): 
        return self.render_figure.render_figure("ajouter/member.html")
    def carnetdadresses(self,search):
        self.render_figure.set_param("address",self.db.Address.getall())
        return self.render_figure.render_figure("ajouter/carnetdadresses.html")
    def addband(self,search):

        return self.render_figure.render_figure("ajouter/band.html")
    def addmusician(self,search):

        return self.render_figure.render_figure("ajouter/musician.html")
    def ajouterenregistrement(self,search):
        getparams=("id",)

        print("get param, action see my new",getparams)
        myparam=self.get_this_route_param(getparams,params)

        try:
          event1="hey"
          self.render_figure.set_param("myid",myparam["id"])
          self.render_figure.set_param("event",event1)
        except:
          print("i missed event")
        return self.render_figure.render_figure("ajouter/enregistrement.html")
    def ajouterlieu(self,search):
        return self.render_figure.render_only_figure("ajouter/lieu.html")
    def ajouterhack(self,search):
        self.render_figure.set_param("personnes",[])
        self.render_figure.set_param("lieux",[])
        return self.render_figure.render_only_figure("ajouter/hack.html")
    def ajouterrumeur(self,search):
        self.render_figure.set_param("personnes",[])
        self.render_figure.set_param("lieux",[])
        return self.render_figure.render_only_figure("ajouter/rumeur.html")
    def nouveau(self,search):
        return self.render_figure.render_figure("welcome/new.html")
    def getlyrics(self,params={}):
        getparams=("id",)

       
        myparam=self.get_this_get_param(getparams,params)
        print("my param :",myparam)
        try:
          print("hey",hey)
          if not hey:
            hey=[]
        except:
          hey=[]

        self.render_figure.set_param("lyrics",hey)
        return self.render_some_json("welcome/lyrics.json")
    def jouerjeux(self,search):
        return self.render_figure.render_figure("welcome/jeu.html")

    def signup(self,search):
        return self.render_figure.render_figure("user/signup.html")
    def signin(self,search):
        return self.render_figure.render_figure("user/signin.html")
    def addpen(self,search):
        return self.render_figure.render_figure("ajouter/pen.html")
    def addnotebook(self,search):
        return self.render_figure.render_figure("ajouter/notebook.html")

    def save_user(self,params={}):
        myparam=self.get_post_data()(params=("username","email","country_id","phone","password","passwordconfirmation"))
        self.user=self.dbUsers.create(myparam)
        if self.user["user_id"]:
            self.set_session(self.user)
            self.set_json("{\"redirect\":\"/\"}")
            return self.render_figure.render_json()
        else:
            self.set_json("{\"redirect\":\"/\"}")
            return self.render_figure.render_json()
    def joueraujeu(self,params={}):
        self.set_json("{\"redirect\":\"/signin\"}")
        getparams=("song_id","jeu_id")
        myparam=self.get_post_data()(params=getparams)
        self.set_session_params(myparam)
        #self.set_redirect("/signin")
        #return self.render_figure.render_redirect()
        return self.render_figure.render_my_json("{\"redirect\":\"/signin\"}")
    def run(self,redirect=False,redirect_path=False,path=False,session=False,params={},url=False,post_data=False):
        if post_data:
            print("post data")
            self.set_post_data(post_data)
            print("post data set",post_data)
        if url:
            print("url : ",url)
            self.Program.set_url(url)
        self.set_my_session(session)

        if redirect:
            self.redirect=redirect
        if redirect_path:
            self.redirect_path=redirect
        if not self.render_figure.partie_de_mes_mots(balise="section",text=self.Program.get_title()):
            self.render_figure.ajouter_a_mes_mots(balise="section",text=self.Program.get_title())
        if path and path.endswith("png"):
            self.Program=Pic(path)
            self.Program.set_path("./")
        elif path and path.endswith("mp4"):
            self.Program=Vid(path)
            self.Program.set_path("./")
        elif path and path.endswith("mp3"):
            self.Program=Music(path)
            self.Program.set_path("./")
        elif path and path.endswith("webp"):
            self.Program=Pic(path)
            self.Program.set_path("./")
        elif path and path.endswith("jpeg"):
            self.Program=Pic(path)
            self.Program.set_path("./")
        elif path and path.endswith("gif"):
            self.Program=Pic(path)
            self.Program.set_path("./")
        elif path and path.endswith("svg"):
            self.Program=Pic(path)
            self.Program.set_path("./")
        elif path and path.endswith("jpg"):
            self.Program=Pic(path)
            self.Program.set_path("./")
        elif path and path.endswith(".jfif"):
            self.Program=Pic(path)
        elif path and path.endswith(".css"):
            self.Program=Css(path)
        elif path and path.endswith(".js"):
            self.Program=Js(path)
        elif path:
            path=path.split("?")[0]
            print("link route ",path)
            ROUTES={
            '^/createvideo$': self.createvideo,
            '^/addvideo$': self.addvideo,
            "^/seevideo/([0-9]+)$":self.seevideo,
            '^/welcome$': self.welcome,
            '^/sign_in$': self.signin,
            '^/sign_up$': self.signup,
            '^/logmeout$':self.logout,
            '^/signup$':self.save_user,
            '^/save_user$':self.save_user,
            '^/update_user$':self.update_user,
            "^/seeuser/([0-9]+)$":self.seeuser,
            "^/edituser/([0-9]+)$":self.edit_user,
            "^/deleteuser/([0-9]+)$":self.delete_user,
            '^/login$':self.login,
            '^/users$':self.myusers,
            '^/$': self.hello
            }
            REDIRECT={"/save_user": "/welcome"}
            for route in ROUTES:
               print("pattern=",route)
               mycase=ROUTES[route]
               x=(re.match(route,path))
               print(True if x else False)
               
               if x:
                   params["routeparams"]=x.groups()
                   try:
                       html=mycase(params)
                       print("html bon")
                       #print(html)
                   except Exception as e:  
                       print("erreur"+str(e),traceback.format_exc())
                       html=("<p>une erreur s'est produite dans le code server  "+(traceback.format_exc())+"</p><a href=\"/\">retour à l'accueil</a>").encode("utf-8")
                       print("html mauvais")
                   
                   self.Program.set_html(html=html)
                   self.Program.clear_notice()
                   return self.Program
               else:
                   self.Program.set_html(html="<p>la page n'a pas été trouvée</p><a href=\"/\">retour à l'accueil</a>")
        return self.Program
