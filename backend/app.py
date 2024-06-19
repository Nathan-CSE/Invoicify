from flask import Flask, jsonify
from models import setup_db
from src.auth import RegisterAPI, LoginAPI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.add_url_rule('/register', view_func=RegisterAPI.as_view('register_api'), methods=['POST'])
app.add_url_rule('/login', view_func=LoginAPI.as_view('login_api'), methods=['POST'])




if __name__ == '__main__':
    # setup_db()
    app.run(debug=True, use_reloader=False)
