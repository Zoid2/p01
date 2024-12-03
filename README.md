# Spanish Studying Service<sup>TM</sup> By Team eColi

# Roster

Ziyad H. (PM): Database backend  
Naf M.: HTML/CSS frontend   
Chloe W.: Flask server and python middleware  
Jayden Z.: Flask server and python middleware   

# Site Description

Our site is an interative Spanish studying service that offers users lessons, flashcards, and quizzes. It employs Merriam-Webster’s Spanish-English Dictionary API to retrieve Spanish-to-English and English-to-Spanish translations, as well as linguistic data for each word. It also uses the Unsplash API to procure relevant images for each vocabulary word, in addition to the Datamuse API to find words and phrases that can be used in tandem with a given term. Users can create an account to save their progress.

# Install Guide

1. Clone and move into this repository
```
$ git clone git@github.com:Zoid2/p01.git
```
```
$ cd p01
```
3. Create and activate a virtual environment
```
$ python3 -m venv foo
```
```
$ . foo/bin/activate
```
5. Install required packages
```
$ pip install -r requirements.txt
```

# Launch Codes

1. Run the Flask app
```
$ python3 app/__init__.py
```
2. Navigate to localhost: http://127.0.0.1:5000
