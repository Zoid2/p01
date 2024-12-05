import os
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__) 
secret = os.urandom(32)
app.secret_key = secret

@app.route("/")
def home():
    user = '' 
    if(session.get('username') != None) {
        user = session.get('username')
        }
    return("index.html", username=user)

@app.route("/response" , methods=['POST'])
def register():
    return render_template('signup.html')

@app.route("/login")
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