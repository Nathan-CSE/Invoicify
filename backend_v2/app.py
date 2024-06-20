import os
from models import db
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from src.auth import RegisterAPI, LoginAPI
from dotenv import load_dotenv

load_dotenv()

def create_app(db_path="database.db"):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.add_url_rule('/register', view_func=RegisterAPI.as_view('register_api'), methods=['POST'])
    app.add_url_rule('/login', view_func=LoginAPI.as_view('login_api'), methods=['POST'])
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)