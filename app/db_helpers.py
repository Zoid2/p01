from flask import session
import sqlite3

#Create SQLite Table, creates if not already made
db = sqlite3.connect("database.db")
cursor = db.cursor()

#Create a User Table
def userTable():
    cursor.execute("CREATE TABLE users(id, name, username)")