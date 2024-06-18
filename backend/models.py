from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

class Invoice(Base):
    __tablename__ = 'invoice'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    fields = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    is_ready = Column(Boolean, nullable=False)

engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def setup_db():
    users = [
        {'username': 'user1', 'password': 'pass1'},
        {'username': 'user2', 'password': 'pass2'},
        {'username': 'user3', 'password': 'pass3'}
    ]

    for user_data in users:
        session.add(User(**user_data))

    invoices = [
        {'name': 'Invoice 001', 'fields': '{"Field A": "Value A", "Field B": "Value B"}', 'user_id': 1, 'is_ready': True},
        {'name': 'Invoice 002', 'fields': '{"Field C": "Value C", "Field D": "Value D"}', 'user_id': 2, 'is_ready': False},
        {'name': 'Invoice 003', 'fields': '{"Field E": "Value E", "Field F": "Value F"}', 'user_id': 3, 'is_ready': True}
    ]
    for invoice_data in invoices:
        session.add(Invoice(**invoice_data))

    session.commit()

