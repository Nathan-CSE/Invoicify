import sys

from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from dotenv import load_dotenv

from models import db
from src.api.auth import auth_ns
from src.api.invoice import invoice_ns

load_dotenv()

def create_app(db_path="database.db"):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    CORS(app)
    
    db.init_app(app)
    with app.app_context():
        db.create_all()

    api = Api(app, validate=True, strict=True, security='apikey', authorizations={
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorisation'
        }
    })
    api.add_namespace(auth_ns)
    api.add_namespace(invoice_ns)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True,host='0.0.0.0')