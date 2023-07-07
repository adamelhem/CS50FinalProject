
import os
from cs50 import SQL,get_string
from flask import Flask, redirect, render_template, request, session
import math

# App Config
app = Flask(__name__)

# Auto-reload Templates
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key ="wow"
app.config["SESSION_TYPE"] = "filesystem"


# Config cs50 lib to use SQLite db
db = SQL("sqlite:///finalproject.db")

@app.route("/", methods=["GET", "POST"])
def index():
    # The user post his answer
    if request.method == "POST":
        # Get the user answer/score/quizid from form
        answer = request.form.get("answer")
        score = session["score"]
        quizid = session["quizid"]

        # Get question from database
        quizPrev = db.execute("select question from questions where id = ?", quizid)[0]["question"]

        # Compare user answered word with Quiz first word
        correctAnswer = answer == quizPrev.split()[0]
        if correctAnswer:
            # Calculate the text readability
            grade = Coleman_Liau_index(quizPrev)
            score += grade
            quizid += 1
            # Save new values of scre and quiz id
            session["score"] = score
            session["quizid"] = quizid
        else:
            result = "Wrong Answer!"
            # Encrypt question from db to send it to the user
            quizEncipher = encipher(quizid, quizPrev)
            # Return new question with the updated score and result
            return render_template("index.html", question = quizEncipher, result = result, score = score)

        # Get quizCount
        quizCount = session["quizCount"]

        # If we reach end of questions amount we finish the game
        if quizid > quizCount:
            quizEncipher = ""
            result = "Game Over , You Win!"
            return render_template("index.html", question = quizEncipher, result = result, score = score)

        # Get the full question original text from database
        message = db.execute("select question from questions where id = ?", quizid)[0]["question"]

        # Encrypt question from db to send it to the user
        quizEncipher = encipher(quizid, message)

        result="Correct Answer!"

        # Return new question with the updated score and result
        return render_template("index.html", question = quizEncipher, result = result, score = score)

    else:
        result=""
        score=0

        # Get question from the data base
        quizid = 1
        message = db.execute("select question from questions where id = ?", quizid)[0]["question"]

        # Encrypt question from db to send it to the user
        quizEncipher = encipher(quizid, message)

        # Remember last score and quiz id
        if session.get('score') is None:
            session["score"] = score

        session["quizid"] = quizid

        # Get the amount of available questions in the database
        quizCount = db.execute("select COUNT() as count from questions")[0]["count"]
        session["quizCount"] = quizCount

        # Return the question page to the user
        return render_template("index.html", question = quizEncipher, result = result, score = score)

#_________________readability_________________
# Coleman-Liau index of a text designed to output grade level
def Coleman_Liau_index(text):
    text = text.upper()
    str_len = len(text)
    if (str_len == 0):
        return 0
    wordCount = 1
    sentencesCount = 0
    lettersCount = 0
    for i in range(0, str_len):
        c = text[i]
        # count words
        if (c == ' '):
            wordCount += 1
        # count sentences
        else:
            if (c == '.' or c == '!' or c == '?'):
                sentencesCount += 1
            # count letters
            else:
                if ('Z' >= c and c >= 'A'):
                    lettersCount += 1
    # average number of letters per 100 words
    L = (lettersCount / wordCount) * 100
    # average number of letters per 100 words
    S = (sentencesCount / wordCount) * 100
    # Coleman_Liau_index formula
    index = 0.0588 * L - 0.296 * S - 15.8
    index = round(index)
    return index
#________________________________________

#_________________Caesar_________________
# For each character in the plaintext:
# Rotate the character if it's a letter
# Convert given key from a `string` to an array of `int` to demonstrate rotations
# Ci = (Pi + K) % 26
# encipher the text based on the key
def encipher(key, textStr):
    text = list(textStr)
    isValid = only_digits(key)
    if not isValid:
        print("Key must be a digit.\n")
        exit
    keyDigits = convert_to_digits(key)
    strLen = len(text)
    for i in range(strLen):
        t = text[i]
        if (t.isalpha()):
            # Calculate the distanceof the char to rotate the char
            d = rotate(t, keyDigits)
            text[i] = d
        else:
            text[i] = t
    return "".join(text)


# Check if string is only digits
def only_digits(key):
    keyStr = str(key)
    isDigits = not keyStr.isalpha();
    return isDigits


# Convert argv[1] from a `string` to an `int`
def convert_to_digits(key):
    return int(key)


# Rotate char based on the key
def rotate(c, k):
    i = 0
    # Calculate based on lower case char
    if (c.lower() == c):
        lowAlpaDic = "abcdefghijklmnopqrstuvwxyz"
        cInt = lowAlpaDic.find(c)
        i = ((cInt + k) % 26)
        c = lowAlpaDic[i]
    else:
        # Calculate based on upper case char
        lowAlpaDic = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        cInt = lowAlpaDic.find(c)
        i = ((cInt + k) % 26)
        c = lowAlpaDic[i]
    return c
#_________________Caesar_________________
