'''
eColi: Ziyad H, Naf M, Chloe W, Jayden Z
SoftDev
P01: Spanish Studying Service
2024-12-17
Time Spent:
'''

import os
import random
import urllib.request
import json
from flask import Flask, render_template, request, redirect, url_for, session
import db_helpers as db

app = Flask(__name__)
secret = os.urandom(32)
app.secret_key = secret

key_merriam = None
key_unsplash = None

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
    return render_template("signup.html", projectName = "monoLingo")

@app.route("/lesson/<int:page_id>")
def lesson(page_id):
    try:
        with open("keys/key_merriam_webster.txt", "r") as file:
            key_merriam = file.read().strip()
    except:
        return error("Missing key for Merriam-Webster API")
    try:
        with open("keys/key_unsplash.txt", "r") as file:
            key_unsplash = file.read().strip()
    except:
        return error("Missing key for Unsplash API")
    prompt = "car"
    prompt_trans = None
    related = None
    related_trans = None
    image = None
    if key_unsplash:
        try:
            unsplash = urllib.request.urlopen('https://api.unsplash.com/search/photos?page=1&query=' + prompt + '&client_id=' + key_unsplash)
            unsplash_data = json.loads(unsplash.read())
            image = unsplash_data['results'][0]['urls']['raw']
        except:
            print("Issue with Unsplash API")
            #return error("Issue with Unsplash API")
    else:
        return error("File for Unsplash key empty")
    try:
        datamuse = urllib.request.urlopen('https://api.datamuse.com/words?rel_jjb=' + prompt)
        datamuse_data = json.loads(datamuse.read())
        related = datamuse_data[0]['word']
    except:
        print("Issue with Datamuse API")
        #return error("Issue with Datamuse API")
    if key_merriam:
        try:
            merriam_prompt = urllib.request.urlopen('https://www.dictionaryapi.com/api/v3/references/spanish/json/' + prompt + '?key=' + key_merriam)
            merriam_prompt_data = json.loads(merriam_prompt.read())
            if ":" in merriam_prompt_data[0]['shortdef'][0]:
                prompt_trans = merriam_prompt_data[0]['shortdef'][0].split(":")[1]
            else:
                prompt_trans = merriam_prompt_data[0]['shortdef'][0]
            merriam_related = urllib.request.urlopen('https://www.dictionaryapi.com/api/v3/references/spanish/json/' + related + '?key=' + key_merriam)
            merriam_related_data = json.loads(merriam_related.read())
            if ":" in merriam_related_data[0]['shortdef'][0]:
                related_trans = merriam_related_data[0]['shortdef'][0].split(":")[1]
            else:
                related_trans = merriam_related_data[0]['shortdef'][0]
        except:
            print("Issue with Merriam-Webster API")
            #return error("Issue with Merriam-Webster API")
    else:
        return error("File for Merriam-Webster key empty")
    
    # Flashcards

    clicked_card = None
    if request.method == "POST":
        clicked_card = request.form.get("card_key")

    return render_template('lesson.html', prompt = prompt, prompt_trans = prompt_trans, related = related, related_trans = related_trans, image = image, lessonFlashCards = flashCards(page_id), clicked_card=clicked_card)

@app.route("/error")
def error(message):
    return render_template("error.html", error = message)

@app.route("/study/<int:page_id>", methods=["GET", "POST"])
def study(page_id):
    defaultValue = 5
    questionsArr = []
    correctAnswers = []
    imagesArr = []
    wordBank = []
    wordBankDict = db.createDict("./flashcards/lesson_" + str(page_id) + ".csv")
    for i in range(len(wordBankDict.values())):
        randomInt3 = random.randint(0, len(wordBankDict.values()) - 1)
        wordBank.append(list(wordBankDict.values())[randomInt3])
        print(wordBank[i])
        wordBankDict.pop(list(wordBankDict.keys())[randomInt3])

    if request.method == "POST":
        questions = request.form.get("num_questions")
        questionsTotal = int(questions)
    else:
        questionsTotal = defaultValue

    for i in range(questionsTotal):
        randomInt = random.randint(1,2)
        try:
            if randomInt == 1:
                unsplash = urllib.request.urlopen('https://api.unsplash.com/search/photos?page=1&query=' + wordBank[i] + '&client_id=' + key_unsplash)
                unsplash_data = json.loads(unsplash.read())
                image = unsplash_data['results'][0]['urls']['raw']
                imagesArr.append(image)
                correctAnswers.append(wordBank[i])
            else:
                randomInt2 = random.randint(1,2)
                if randomInt2 == 1:
                    questionsArr.append("Translate to Spanish: " + wordBank[i])
                    try:
                        merriam_prompt = urllib.request.urlopen('https://www.dictionaryapi.com/api/v3/references/spanish/json/' + wordBank[i] + '?key=' + key_merriam)
                        merriam_prompt_data = json.loads(merriam_prompt.read())
                        if ":" in merriam_prompt_data[0]['shortdef'][0]:
                            prompt_trans = merriam_prompt_data[0]['shortdef'][0].split(":")[1]
                        else:
                            prompt_trans = merriam_prompt_data[0]['shortdef'][0]
                    except:
                        print("Issue with Merriam-Webster API")
                    correctAnswers.append(prompt_trans)
                else:
                    try:
                        merriam_prompt = urllib.request.urlopen('https://www.dictionaryapi.com/api/v3/references/spanish/json/' + wordBank[i] + '?key=' + key_merriam)
                        merriam_prompt_data = json.loads(merriam_prompt.read())
                        if ":" in merriam_prompt_data[0]['shortdef'][0]:
                            prompt_trans = merriam_prompt_data[0]['shortdef'][0].split(":")[1]
                        else:
                            prompt_trans = merriam_prompt_data[0]['shortdef'][0]
                    except:
                        print("Issue with Merriam-Webster API")
                    questionsArr.append("Translate to English: " + prompt_trans)
                    correctAnswers.append(wordBank[i])
        except:
            print('error with unsplash api')
    return render_template("study.html", questionsArr = questionsArr, correctAnswers = correctAnswers, testID = page_id)

def flashCards(lessonNumber):
    flashCardArray = db.createDict("./flashcards/lesson_" + str(lessonNumber) + ".csv")
    return flashCardArray

@app.route("/submit_test", methods=["POST"])
def submit_test():
    answers = []
    questions = []
    correctAnswers = []
    testID = []
    
    for key, value in request.form.items():
        if key.startswith('answer_'):
            question_index = key.split('_')[1]
            answers[question_index] = value
        elif key.startswith('question_'):
            question_index = key.split('_')[1]
            questions[question_index] = value
        else:
            question_index = key.split('_')[1]
            testID.append(int(key.split('_')[2]))
            correctAnswers[question_index] = value
    
    testName = "test" + testID[0]
    
    db.testTable(testName)
    
    for i in range(len(answers)):
        db.addQuestion(testName, questions[i], answers[i], correctAnswers[i])

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.debug = True
    app.run()
