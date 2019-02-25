from flask import (Flask, Response, request, redirect,
    render_template, session, url_for)
import pyotp
import os
import plivo
import time


app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/phone_verification", methods=["GET", "POST"])
def phone_verification():
    key = 'Plivo Auth ID'
    auth = 'Plivo Auth token'
    client = plivo.RestClient(key, auth)
    if request.method == "POST":
        phone_number = request.form.get("phone_number")
        method = request.form.get("method")

        session['phone_number'] = phone_number
        totp = pyotp.TOTP('base32secret3232')
        otp = totp.now()
        session['otp'] =otp

        if method == 'sms':
            client.messages.create(src='918548844984',dst=phone_number,text= 'Your one time password is'+ ' ' + otp);
        else:
            client.calls.create(from_= '918548854988',to_= phone_number, answer_url= 'http://69b4d38c.ngrok.io/answerurl' )

        return redirect(url_for("verify"))

    return render_template("login.html")

@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
            token = request.form.get("token")
            if session['otp'] == token:
                return Response("<h1>Success!</h1>")

    return render_template("verify.html")


@app.route("/answerurl" , methods= ['GET','POST'])
def answer_url():
    if request.method =="POST":
        totp = pyotp.TOTP('base32secret3232')
        otp = totp.now()
        session['otp'] = otp
        l = session['otp']
        speak = str(list(l))
        response = (plivo.plivoxml.ResponseElement().add(plivo.plivoxml.SpeakElement('One time password is'+speak).set_loop(3)).add(plivo.plivoxml.WaitElement(30)))
    return response.to_string()

if __name__ == '__main__':
    app.run(debug=True)
