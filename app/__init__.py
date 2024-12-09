'''
eColi: Ziyad H, Naf M, Chloe W, Jayden Z
SoftDev
P01: Spanish Studying Service
2024-12-17
Time Spent:
'''

import os
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import db_helpers as db
import urllib.request
import json

app = Flask(__name__) 
secret = os.urandom(32)
app.secret_key = secret

key_merriam = None
try:
    with open("keys/key_merriam_webster.txt", "r") as file:
        key_merriam = file.read().strip()
except:
    print('no merriam key')

key_unsplash = None
try:
    with open("keys/key_unsplash.txt", "r") as file:
        key_unsplash = file.read().strip()
except:
    print('no unsplash key')

@app.route("/")
def home():
    if session.get("username") != None:
        return render_template("index.html", name = session["name"])
    return redirect(url_for("signup"))

@app.route("/response" , methods=['POST', 'GET'])
def register():
    name = request.form.get("name")
    username = request.form.get("username")
    password = request.form.get("password")
    db.addUser(name, username, password)
    session["name"] = name
    session["username"] = username
    session["password"] = password
    return redirect(url_for("home"))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if (session.get('username') != None):
        return redirect(url_for("home"))
    print(request.args)
    print(request.form)
    # The 'usernameL' and 'passwordL' will change when html is sorted
    if request.method == "POST" and db.validateUser(request.form.get("usernameL"), request.form.get("passwordL")):
        session["username"] = request.form.get("usernameL")
        print(session["username"])
        session["name"] = db.getName(session["username"])
        session["password"] = request.form.get("passwordL")
        print("Hello")
        return redirect(url_for("home"))
    return render_template("signin.html")

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    session.pop("password", None)
    session.pop("name", None)
    return redirect(url_for("home"))

@app.route("/signup")
def signup():
    return render_template("signup.html", projectName = "Name PH")

@app.route("/lesson")
def lesson():
    prompt = 'flower'
    datamuse = urllib.request.urlopen('https://api.datamuse.com/words?ml=' + prompt)
    datamuse_data = json.loads(datamuse.read())
    word = datamuse_data[0]['word']
    translation = None
    if key_merriam:
        try:
            merriam = urllib.request.urlopen('https://www.dictionaryapi.com/api/v3/references/spanish/json/' + word + '?key=' + key_merriam)
            merriam_data = json.loads(merriam.read())
            translation = merriam_data[0]['shortdef'][0]
        except:
            print('error with merriam api')
    image = None
    if key_unsplash:
        try:
            unsplash = urllib.request.urlopen('https://api.unsplash.com/search/photos?page=1&query=' + word + '&client_id=' + key_unsplash)
            unsplash_data = json.loads(unsplash.read())
            image = unsplash_data['results'][0]['urls']['raw']
        except:
            print('error with unsplash api')
    return render_template('lesson.html', word = word, translation = translation, image = image)

if __name__ == "__main__":
    app.debug = True
    app.run()