class Directory():
    session=False
    pic=False
    vid=False
    music=False
    redirect=False
    code422=False
    js=False
    nocache=False
    json=False
    css=False
    def __init__(self, title):
        self.title=title
        self.session={"email":"","user_id":"","name":"","notice":""}
        self.path="./"
        self.html=""
        self.url=""
        self.mesparams=["email","name","user_id","notice"]
        self.redirect=False
    def logout(self):
        for x in self.mesparams:
            try:
                self.session[x]=""
            except:
                print("erreur session logout ",x)
                self.session[x]=""
        self.session["notice"]="Vous êtes déconnecté(e)"
        self.session["mysession"]=True
    def not_notice(self):
        self.session["notice"]=""
    def get_session(self):
        return self.session
    def set_other_session(self,s):
        for x in self.mesparams:
            try:
                self.session[x]=s[x]
            except:
                print("erreur session ",x)
                self.session[x]=""
        self.session["mysession"]=False
    def set_my_session(self,s):
        for x in self.mesparams:
            try:
                self.session[x]=s[x]
            except:
                print("erreur session ",x)
                self.session[x]=""
        self.session["mysession"]=False
    def get_session_param(self,s):
        try:
            return self.session[s]
        except:
            return ""
    def set_session_params(self,s):
        for x in s:
            try:
                self.session[x]=s[x]
            except:
                print("erreur session ",x)
                self.session[x]=""
        self.session["mysession"]=True
    def set_session(self,s):
        for x in self.mesparams:
            try:
                self.session[x]=s[x]
            except:
                print("erreur session ",x)
                self.session[x]=""
        self.session["mysession"]=True
    def get_url(self):
        return self.url
    def set_url(self,url):
        self.url=url
    def get_css(self):
        return self.css
    def set_css(self,html):
        self.css=html
    def get_nocache(self):
        return self.nocache
    def set_nocache(self,html):
        self.nocache=html
    def get_json(self):
        return self.json
    def set_json(self,html):
        self.json=html
    def get_code422(self):
        return self.code422
    def set_code422(self,html):
        self.code422=html
    def get_js(self):
        return self.js
    def set_js(self,html):
        self.js=html
    def get_music(self):
        return self.music
    def set_music(self,html):
        self.music=html
    def get_vid(self):
        return self.vid
    def set_vid(self,html):
        self.vid=html
    def get_pic(self):
        return self.pic
    def set_pic(self,html):
        self.pic=html
    def get_html(self):
        return self.html
    def set_html(self,html):
        self.html=html
    def set_redirect(self,red):
        self.redirect=red
        self.html="Moved permanently to <a href=\"{url}\">{url}</a>".format(url=red)
    def get_redirect(self):
        return self.redirect
    def set_path(self,path):
        self.path=path
    def get_title(self):
        return self.title
    def get_path(self):
        return self.path
    def clear_notice(self):
        mysession=self.get_session()
        print("url : : ",self.url)
        print("session : : ",mysession)
        if not mysession["mysession"]:
            self.session["notice"]=""
    def redirect_if_not_logged_in(self):
        mysession=self.get_session()
        if (not mysession or mysession and (int("0"+str(mysession["user_id"])) == 0)) and not self.redirect and self.url not in ["/","/youbank","/youbank_inscription","/cartedidentite"] and self.url in ["/fill_in_inbox","/post_hom_office","/tweet_details"]:
            print("ok not loged in")
            redi="/youbank"
            self.redirect=redi
            self.html="Moved permanently to <a href=\"{url}\">{url}</a>".format(url=redi)
            self.session["notice"]="vous n'êtes pas connecté"
