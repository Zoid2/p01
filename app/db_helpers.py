import sqlite3
from flask import session
import bcrypt


#Create SQLite Table, creates if not already made
db = sqlite3.connect("database.db", check_same_thread=False)
cursor = db.cursor()

#Create a User Table
def userTable():
    cursor.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT NOT NULL, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)")
    db.commit()
#Create a Lesson Table
def lessonTable():
    cursor.execute("CREATE TABLE lessons(id INTEGER PRIMARY KEY, title TEXT NOT NULL, completion INTEGER, flashcards TEXT)")
    db.commit()

#Create Test Table
def testTable():
    cursor.execute("CREATE TABLE tests(id INTEGER PRIMARY KEY, questions TEXT, correctAnsweres INTEGER)")
    db.commit()

def addUser(name, username, password):
    cursor.execute("INSERT INTO users(name, username, password) VALUES (?, ?, ?)", (name, username, hashPassword(password)))
    db.commit()

def removeUser(id):
    cursor.execute(f"DELETE FROM users WHERE id='{id}'")
    db.commit()

def validateUser(username, password):
    dbPassword = getHash(username)
    if dbPassword:
        return validatePassword(dbPassword, password)
    return False

def getName(username):
    return cursor.execute(f"SELECT name FROM users WHERE username='{username}'").fetchone()[0]

def getHash(username):
    return cursor.execute(f"SELECT password FROM users WHERE username='{username}'").fetchone()[0]

#error?
def hashPassword(password):
    bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashedPassword = bcrypt.hashpw(bytes, salt)
    return hashedPassword

def validatePassword(hash, password):
    print("Password: " + password)
    print("Matches Hash: " + str(bcrypt.checkpw(password.encode("utf-8"), hash)))
    return bcrypt.checkpw(password.encode("utf-8"), hash)

#userTable()
