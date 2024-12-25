from flask import Flask,render_template,request,session,g,redirect,url_for
from savemanager import SaveManager
from utils import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


gonderici_email = "vallabenoguzhanim@gmail.com"
gonderici_sifre = "uqxgqfjqolpbspoy"  # Gmail uygulama şifresi

def sendMail(alici_email,id):
    konu = "Teknik Servis"
    metin = f"Talebinizi sorgulamak icin '{id}' sayısını sorgulayınız"

    # E-posta oluşturma
    mesaj = MIMEMultipart()
    mesaj["From"] = gonderici_email
    mesaj["To"] = alici_email
    mesaj["Subject"] = konu

    # Mesaj içeriği ekleme
    mesaj.attach(MIMEText(metin, "plain"))

    # SMTP sunucusuna bağlanma ve e-posta gönderme
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Güvenli bağlantı başlatma
            server.login(gonderici_email, gonderici_sifre)
            server.sendmail(gonderici_email, alici_email, mesaj.as_string())
            print("E-posta başarıyla gönderildi!")
    except Exception as e:
        print("E-posta gönderilemedi:", str(e))


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
        for i in sm.requests:
            if i.id == int(request.form["takipNo"]):
                return render_template("ResultOFRequest.html",request=i)
        return "Böyle Bir Talep Bulunamadı"

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

@app.route("/add-request",methods=["GET","POST"])
def addRequestPage():
    if not g.personel:
        return redirect(url_for("loginPage"))
    else:
        if request.method == 'POST':

            sm.AddRequest(request.form["name"],request.form["type"],request.form["mail"],request.form["personelId"],request.form["definition"])

            sendMail(sm.requests[-1].mail,sm.requests[-1].id)

            return redirect(url_for("dashboard"))
        else:
            return render_template("addRequest.html",personels=sm.personeller)
            
@app.route("/delete-request/<id>")
def deleteRequest(id):
    if not g.personel:
        return redirect(url_for("loginPage"))
    else:
        index=0
        for i in sm.requests:
            if i.id == int(id):
                sm.requests.pop(index)
                break
            else:
                index+=1
        return redirect(url_for("dashboard"))
app.run()