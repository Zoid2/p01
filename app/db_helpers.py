from flask import session
import sqlite3

#Create SQLite Table, creates if not already made
db = sqlite3.connect("database.db", check_same_thread=False)
cursor = db.cursor()

#Create a User Table
def userTable():
    cursor.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT NOT NULL, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)")
    db.commit()

def addUser(name, username, password):
    cursor.execute("INSERT INTO users(name, username, password) VALUES (?, ?, ?)", (name, username, password))
    db.commit()

def removeUser(id):
    cursor.execute(f"DELETE FROM users WHERE id='{id}'")
    db.commit()


#userTable()