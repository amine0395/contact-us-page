import requests
from flask import Flask , redirect ,url_for,render_template,request
import datetime
import smtplib
app = Flask(__name__)
Ur_email = "Ur email"
Ur_password="Ur password"
Dest_email="the destination email for your client support"

@app.route("/")
def home():
    return "<h1>main</h1>"
@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        user = request.form["name"]
        email= request.form["email"]
        text = request.form["message"]
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=Ur_email, password=Ur_password)
        a=requests.get(f"https://api.genderize.io?name={user}")
        gender=a.json()["gender"]
        if gender == "null":
            gender="unidentified"
        connection.sendmail(from_addr=Ur_email, to_addrs=Dest_email,msg="".join(("subject: client message \n \n ","name:",user,"  gender=",gender,"\n email:",email,"\n message:",text)).encode('utf-8'))
        connection.close()
        return redirect(url_for("user",usr=user))
    else:
        return render_template("index.html",year=datetime.date.today().year)
@app.route("/registered/<usr>")
def user(usr):
    return render_template("registered.html",usr=usr,year=datetime.date.today().year)

if __name__ == "__main__":
    app.run(debug=True)
