from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Table, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('sqlite:///data.db')

Session = sessionmaker(bind=engine)
session = Session()

BaseModel = declarative_base()

class User(BaseModel):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    teacher = Column(String(100))
    password = Column(Text)

    exam = relationship('Event', back_populates='teacher')


class Event(BaseModel):
    __tablename__ = 'event'

    event_id = Column(Integer, primary_key=True)
    event = Column(Text)
    date_time = Column(DateTime, default=datetime.now)

    teacher_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    teacher = relationship('User', back_populates='exam')

def init_db():
    engine = create_engine("sqlite:///data.db")
    BaseModel.metadata.create_all(engine)

def get_connection():
    engine = create_engine("sqlite:///data.db")
    BaseModel.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()