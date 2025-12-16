from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

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
    presence = Column(Boolean, default=True)
    reason = Column(Text, default=None)

    # Исправлено: ссылаемся на первичный ключ пользователя
    teacher_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    admin_id = Column(Integer, ForeignKey('admin.id'), nullable=False)

    teacher = relationship('User', back_populates='event')


# Создаем engine один раз
engine = create_engine('sqlite:///data.db', echo=False)
Session = sessionmaker(bind=engine)


def init_db():
    BaseModel.metadata.create_all(engine)


def get_connection():
    """Создает и возвращает новую сессию"""
    return Session()