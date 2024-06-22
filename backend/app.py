import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from dotenv import load_dotenv

from src.auth import auth_ns
from models import db

load_dotenv()

def create_app(db_path="database.db"):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    api = Api(app)
    CORS(app)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    api.add_namespace(auth_ns)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)