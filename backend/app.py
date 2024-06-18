from flask import Flask, jsonify
from models import setup_db

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    setup_db()
    app.run(debug=True, use_reloader=False)
