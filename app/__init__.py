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

app = Flask(__name__) 
secret = os.urandom(32)
app.secret_key = secret

@app.route("/")
def home():
    user = session.get('username', '')
    return render_template("index.html", username=user)

@app.route("/register", methods=['GET', 'POST'])
def register():
    return render_template("signup.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if(session.get('username') != None):
        return redirect(url_for("home"))
    return render_template("signin.html")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return render_template("logout.html")

if __name__ == "__main__":
    app.debug = True
    app.run()