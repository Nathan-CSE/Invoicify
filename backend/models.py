from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

class Invoice(db.Model):
    __tablename__ = 'invoice'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    fields = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_ready = db.Column(db.Boolean, nullable=False)

class ValidationAccessToken(db.Model):
    __tablename__ = "validation_access_token"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)