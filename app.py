from functools import wraps
import sys
import os
from flask import Flask, render_template, url_for, session, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import pyrebase
import cv2
import json
import numpy as np
import base64
from convert import * 
import random
import string

config = {
    "apiKey": "AIzaSyBN-e5-pkWHMXFACF_95xrwO8NqInvPknI",
    "authDomain": "vandyhack-55bc4.firebaseapp.com",
    "databaseURL": "https://vandyhack-55bc4.firebaseio.com",
    "projectId": "vandyhack-55bc4",
    "storageBucket": "vandyhack-55bc4.appspot.com",
    "messagingSenderId": "155180542051",
    "appId": "1:155180542051:web:ad029ccc7f22cd6a8d3056",
    "measurementId": "G-7RXQ81QGGM"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth() 
db = firebase.database()
app = Flask(__name__)
#app secret key
app.secret_key = os.urandom(24)


def isAuthenticated(f):
    @wraps(f)
    def decorated_function(*args, **kwargs): 
        if not auth.current_user != None: 
            return redirect(url_for('signup'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    return redirect(url_for('login'))


@app.route("/register", methods = ["GET", "POST"])
def signup(): 
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        confpassword = request.form["confpassword"]
        try:
            if password != confpassword: 
                return render_template('register.html', message = "The Passwords Don't Match, Please Try Again")
            elif len(password) < 6: 
                return render_template('register.html', message = "Password Must be At Least 6 Characters")
            auth.create_user_with_email_and_password(email, password)
            db.child("user").child(email.replace(".", ",")).push({
                "email": email, 
                "session": "",
                "notes": ""
            })
            return redirect("/login")
        except: 
            return render_template('register.html', message = "This Account is already taken, Please try another.")
    elif request.method == "GET":
        return render_template('register.html')

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        #get the request data
        email = request.form["email"]
        password = request.form["password"]
        try:
            #login the user
            user = auth.sign_in_with_email_and_password(email, password)
            #set the session
            user_id = user['idToken']
            user_email = email
            session['usr'] = user_id
            session["email"] = user_email
            return redirect("/main")  
        except:
            return render_template("login.html", message="This User Doesn't Exist")  
    else:
        return render_template("login.html")

@app.route("/logout")
def logout(): 
    auth.current_user = None
    session.clear()
    user.redirect("/login")

@app.route("/main", methods=["GET", "POST"])
def main(): 
    return render_template("main.html")

def save(encoded_data, filename):
    img = cv2.imdecode(encoded_data, cv2.IMREAD_ANYCOLOR)
    return cv2.imwrite(filename, img)

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

@app.route("/getimg/<theid>", methods = ["POST"])
def getimg(theid): 
    datajson = request.get_json(force=True)
    img = datajson[22:]
    imgdata = base64.b64decode(img)
    filename = 'canvas.png'  # I assume you have a way of picking unique filenames
    with open(filename, 'wb') as f:
        f.write(imgdata)
    string = changeimg()
    print(string)
    os.remove('canvas.png')
    ordereddict = db.child("sessions").child(theid).get()
    array = [v for k,v in ordereddict.val().items()][0]
    db.child("sessions").child(theid).remove()
    db.child("sessions").child(theid).push({
        "users": array["users"],
        "livetext": string,
        "cumulativetext": array["cumulativetext"],
        "tostudent": array["tostudent"]
    })
    return 'hi'


@app.route("/create", methods = ["get"])
@isAuthenticated
def makesession(): 
    id = get_random_string(5)
    user = db.child("user").child(session["email"].replace(".", ",")).get()
    array = [v for k,v in user.val().items()][0]
    notes = array['notes']
    post = {
        "email": session["email"], 
        "session": id,
        "notes": notes
    }
    db.child("user").child(session["email"].replace(".", ",")).remove()
    db.child("user").child(session["email"].replace(".", ",")).push(post)

    db.child("sessions").child(id).push({
        "users": session["email"],
        "livetext": "",
        "cumulativetext": "",
        "tostudent": ""
    })
    return redirect("sessionroom/" + id)

@app.route("/sessionroom/<id>", methods=["GET"])
def sessionroom(id): 
    ordereddict = db.child("sessions").child(id).get()
    array = [v for k,v in ordereddict.val().items()][0]
    print(array['livetext'])
    return render_template("session.html", id = id, data = array['livetext'])

@app.route("/saveforstudent", methods = ["POST"])
def saveforstudent(): 
    datajson = request.get_json(force=True)
    value = datajson['data']
    id = datajson['theid']
    database = db.child("sessions").child(id).get()
    array = [v for k,v in database.val().items()][0]
    db.child("sessions").child(id).remove()
    db.child("sessions").child(id).push({
        "users": array["users"],
        "livetext": array["livetext"],
        "cumulativetext": array["cumulativetext"] + value,
        "tostudent": value
    })
    return 'done'

@app.route("/stopsession/<id>", methods = ["GET"])
def stopsession(id):
    database = db.child("sessions").child(id).get()
    db.child("sessions").child(id).remove()
    array = [v for k,v in database.val().items()][0]
    userlst = array["users"].split(";")
    db.child("notes").child(id).push({
        "content": array["cumulativetext"],
        "title": "Note At " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    })
    for user in userlst: 
        database2 = db.child("user").child(user.replace(".", ",")).get()
        array2 = [v for k,v in database2.val().items()][0]
        db.child("user").child(user.replace(".", ",")).remove()
        db.child("user").child(user.replace(".", ",")).push({
            "email": user,
            "notes": id,
            "session": ""
        })
    return redirect(url_for('main'))

@app.route("/joinlec", methods = ["POST"])
def joinlec(): 
    id = request.form["code"]
    try:
        database = db.child("sessions").child(id).get()
        array = [v for k,v in database.val().items()][0]
        db.child("sessions").child(id).remove()
        db.child("sessions").child(id).push({
            "users": array["users"] + session["email"],
            "livetext": array["livetext"],
            "cumulativetext": array["cumulativetext"],
            "tostudent": array["tostudent"]
        })
        return redirect("lecture/" + id)
    except:
        return render_template("main.html", notfound = "This Session Does Not Exist")

@app.route("/lecture/<id>", methods = ["GET"])
def lecture(id): 
    return render_template("base.html", id = id)

@app.route("/getlecturemessage/<id>", methods = ["GET"])
def getlecturemessage(id): 
    database = db.child("sessions").child(id).get()
    array = [v for k,v in database.val().items()][0]
    print(array['tostudent'])
    return render_template("base.html", id = id, data = array['tostudent'])




if __name__ == "__main__": 
    app.run(debug = True)