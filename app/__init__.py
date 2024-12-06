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

app = Flask(__name__) 
secret = os.urandom(32)
app.secret_key = secret

@app.route("/")
def home():
    if session.get("username") != None:
        return render_template("index.html")
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
    return render_template("signin.html")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return render_template("logout.html")

@app.route("/signup")
def signup():
    return render_template("signup.html", projectName = "Name PH")

if __name__ == "__main__":
    app.debug = True
    app.run()