from flask import Flask,render_template,request,session,g,redirect,url_for
from savemanager import SaveManager
from utils import *
sm=SaveManager()

if len(sm.personeller) ==0:
    print("Bir root kullanici gereklidir")
    psw=input(">>>")
    sm.AddPersonel("root",psw,"ANY",True)

app = Flask(__name__)
app.secret_key="1234"

@app.before_request
def before_request():
    if "id" in session:
        personel = [x for x in sm.personeller if x.id==session["id"]][0]
        g.personel=personel
    else:
        g.personel=None

@app.route("/")
def mainPage():
    return render_template("index.html")

@app.route("/sorgula",methods=['GET', 'POST'])
def queryPage():
    if request.method == 'POST':
        return "Sorgu Yapılıyor...."
    else:
        return render_template("sorgu.html")

@app.route("/login",methods=["GET","POST"])
def loginPage():
    if request.method == 'POST':
        session.pop("id",None)

        username=request.form['username']
        password=request.form['password']

        personeler = [x for x in sm.personeller if x.username==username]
        if len(personeler)==1:
            if(personeler[0].password==password):
                session["id"]=personeler[0].id
                return redirect(url_for("dashboard"))
        return render_template("login.html",hata="Kullanıcı adı veya şifre hatalı")
    else:
        return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if not g.personel:
        return redirect(url_for("loginPage"))
    else:
        return render_template("dashboard.html",requests=sm.requests,admin=g.personel.yetki)

app.run()