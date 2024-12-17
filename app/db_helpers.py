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
    cursor.execute("CREATE TABLE lessons(id INTEGER PRIMARY KEY, title TEXT NOT NULL, content TEXT, completion INTEGER, flashcards TEXT)") # flashcards should be csv file location
    db.commit()

#Create Test Table
def testTable0():
    cursor.execute("CREATE TABLE tests(id INTEGER PRIMARY KEY, questions TEXT, correctAnswers INTEGER)") # questions should be csv file location
    db.commit()

def testTable(name):
    cursor.execute(f"CREATE TABLE '{name}'(id INTEGER PRIMARY KEY, question TEXT, userAnswer TEXT, correctAnswer TEXT)")
    db.commit()

# User Helpers

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

def getId(username):
    return cursor.execute(f"SELECT id FROM users WHERE username='{username}'").fetchone()[0]

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

# End of User Helpers

# Lesson Helpers

def addLesson(title, content, flashcards):
    cursor.execute("INSERT INTO lessons(title, content, flashcards) VALUES (?, ?, ?)", (title, content, flashcards))
    db.commit()

def getLesson(id):
    return cursor.execute("SELECT content FROM lessons WHERE id=?", (id,)).fetchone()[0]

def csvText(csv): # Takes csv file location, returns array of flashcards with each term being a card e.g. [spanish, english]
    text = open(csv, "r")
    return text.read()

def createDict(csv): # Takes csv file location, returns dictionary with first csv term as the key and the second as the value
    output = {}
    flashArray = csvText(csv).splitlines()
    for i in range(len(flashArray)):
        card = flashArray[i]
        output[card[:card.index(",")]] = card[card.index(",") + 1:] # Splices each flashcard into a front and back, and creates a dictionary entry
    return output

# End of Lesson Helpers

# Test Helpers

def addQuestion(table, question, userAnswer, correctAnswer):
    cursor.execute(f"INSERT INTO '{table}'(question, userAnswer, correctAnswer) VALUES ('{question}', '{userAnswer}', '{correctAnswer}')")
    db.commit()

def getQuestions(table):
    numRows = cursor.execute(f"SELECT COUNT(*) FROM '{table}'").fetchone()[0]
    output = []
    for i in range(1, numRows + 1):
        question = cursor.execute(f"SELECT question FROM '{table}' WHERE id=" + str(i)).fetchone()[0]
        output.append(question)
    return output

def getAnswers(table):
    numRows = cursor.execute(f"SELECT COUNT(*) FROM '{table}'").fetchone()[0]
    output = []
    for i in range(1, numRows + 1):
        userAnswer = cursor.execute(f"SELECT userAnswer FROM '{table}' WHERE id=" + str(i)).fetchone()[0]
        output.append(userAnswer)
    return output

def getCorrectAnswers(table):
    numRows = cursor.execute(f"SELECT COUNT(*) FROM '{table}'").fetchone()[0]
    output = []
    for i in range(1, numRows + 1):
        correctAnswer = cursor.execute(f"SELECT correctAnswer FROM '{table}' WHERE id=" + str(i)).fetchone()[0]
        output.append(correctAnswer)
    return output

def displayAllTables():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    tableNames = [table[0] for table in tables]  # Extract table names from result
    print(tableNames)
    return tableNames

# End of Helpers

#userTable()
#lessonTable()
#testTable()
