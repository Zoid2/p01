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

@app.before_first_request
def create_lessons():
    lessons = [
        {
            "title": "Lesson 1: Animals",
            "content": "krjfwlr",
            "flashcards": "flashcards/lesson_1.csv"  
        },
        {
            "title": "Lesson 2: Food",
            "content": "wlekjrbg",
            "flashcards": "flashcards/lesson_2.csv"
        }
    ]
    for lesson in lessons:
        db.addLesson(lesson["title"], lesson["content"], lesson["flashcards"])
    
@app.route("/")
def home():
    if session.get("username") != None:
        allTables = db.displayAllTables()
        userID = db.getId(session.get("username"))
            
        testTables = []
        questions = [[]]
        userAnswers = [[]]
        correctAnswers = [[]]
        correctAnswersAmount = []

        for table in allTables:
            if table.endswith(userID):
                testTables.append(table[4:])
                questions.append(db.getQuestions(table))
                userAnswers.append(db.getAnswers(table))
                correctAnswers.append(db.getCorrectAnswers(table))

        for i in range(len(testTables)):
            correct = 0
            for j in range(len(userAnswers)):
                for k in range(len(userAnswers[i])):
                    if userAnswers[i][j][k].strip().lower() == correctAnswers[i][j][k].strip().lower():
                        correct+=1
            correctAnswersAmount.append(correct)
            
        return render_template("index.html", name = session["name"], questions = questions, 
                               userAnswers = userAnswers, correctAnswers = correctAnswers, 
                               testNumber = testTables, correctAnswersAmount = correctAnswersAmount)
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
    try:
        if request.method == "POST" and db.validateUser(request.form.get("usernameL"), request.form.get("passwordL")):
            session["username"] = request.form.get("usernameL")
            print(session["username"])
            session["name"] = db.getName(session["username"])
            session["password"] = request.form.get("passwordL")
            print("Hello")
            return redirect(url_for("home"))
    except:
        return render_template("error.html", error="Invalid Credentials")
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

@app.route("/search", methods=['GET', 'POST'])
def search():
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
    prompt = request.args.get("word", "alligator")
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
    return render_template('search.html', prompt = prompt, prompt_trans = prompt_trans, related = related, related_trans = related_trans, image = image)

@app.route("/lesson/<int:page_id>", methods=['GET', 'POST'])
def lesson(page_id):
    clicked_card = None
    if request.method == "POST":
        clicked_card = request.form.get("card_key")
    lesson = db.getLesson(page_id+2)
    print(lesson)
    if not lesson:
        error("Lesson not available")
    flashcards = flashCards(page_id)
    return render_template('lesson.html', lessonFlashCards = flashcards, clicked_card=clicked_card)

@app.route("/error")
def error(message):
    return render_template("error.html", error = message)

@app.route("/study/<int:page_id>", methods=["GET", "POST"])
def study(page_id):
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

    defaultValue = 5
    questionsArr = []
    correctAnswers = []
    imagesArr = {}
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
                questionsArr.append("Identify the object in the picture:")
                imagesArr.update({len(questionsArr):image})
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
    print(len(correctAnswers))
    print(len(questionsArr))
    return render_template("study.html", questionsArr = questionsArr, correctAnswers = correctAnswers, testID = page_id, imagesArr = imagesArr)

def flashCards(lessonNumber):
    flashCardArray = db.createDict("./flashcards/lesson_" + str(lessonNumber) + ".csv")
    return flashCardArray

@app.route("/submit_test", methods=["POST"])
def submit_test():
    answers = []
    questions = []
    correctAnswers = []
    testID = None
    
    for key, value in request.form.items():
        if key.startswith('answer_'):
            answers.append(value)
        elif key.startswith('question_'):
            questions.append(value)
        elif key.startswith('correct_'):
            correctAnswers.append(value)
        else:
            testID = int(key.split('_')[1])
    
    testName = "test" + str(testID) + "_" + str(db.getId(session.get("username")))
    
    db.testTable(testName)
    
    for i in range(len(answers)):
        db.addQuestion(testName, questions[i], answers[i], correctAnswers[i])

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.debug = True
    app.run()
