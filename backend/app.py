from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
con = sqlite3.connect("database.db")

def setupDB(con):
    # TODO
    pass

setupDB(con)

@app.route('/')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)