from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Table, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('sqlite:///data.db')
Session = sessionmaker(bind=engine)
session = Session()
BaseModel = declarative_base()

class User(BaseModel): # База данных учителей
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, default=0)
    teacher = Column(String(100))

    event = relationship('Event', back_populates='teacher')


class Admin(BaseModel): # База данных админов
    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, default=0)


class Event(BaseModel): # База данных событий
    __tablename__ = 'event'

    event_id = Column(Integer, primary_key=True)
    text = Column(Text)
    date_time_event = Column(DateTime)
    date_time_add = Column(DateTime, default=datetime.now)

    teacher_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)

    teacher = relationship('User', back_populates='event')


def init_db():
    engine = create_engine("sqlite:///data.db")
    BaseModel.metadata.create_all(engine)

def get_connection():
    engine = create_engine("sqlite:///data.db")
    BaseModel.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()