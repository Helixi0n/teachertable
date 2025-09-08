from database import get_connection, User, Event
from sqlalchemy import delete, update
from datetime import datetime

session = get_connection()

class Model:
    @staticmethod
    def add_teacher(teacher_name, password):
        teacher = User(teacher=teacher_name, password=password)
        session.add(teacher)
        session.commit()
        session.close() # Добавление учителя в сисему

    @staticmethod
    def delete_teacher(teacher_id):
        session.query(User).filter(User.id == teacher_id).delete()
        teacher = session.query(User).filer(User.id == teacher_id).first()
        session.query(Event).filter(Event.teacher_id == teacher.id).delete() 
        session.commit()
        session.close() # Удаление учителя из системы

    @staticmethod
    def sign_in(teacher_id, password, user_id): # Вход
        teacher = session.query(User).filter(User.id == teacher_id).first()

        if teacher.password != password:
            return False # Вывод: неправильный пароль
        else:
            stmt = update(User).where(User.id == teacher_id).values(user_id=user_id)
            session.execute(stmt)
            session.commit()
            session.close()
            return True # Успешный вход
        
    @staticmethod
    def sign_out(user_id):
        stmt = update(User).where(User.user_id == user_id).values(user_id=0)
        session.execute(stmt)
        session.commit()
        session.close() # Выход из системы в главное меню

    @staticmethod
    def change_password(user_id, new_password):
        user = session.query(User).filter(User.user_id == user_id).first()

        if user.password == new_password:
            return False # Пароль совпадает со старым
        else:
            stmt = update(User).where(User.user_id == user_id).values(password=new_password)
            session.execute(stmt)
            session.commit()
            session.close()
            return True # Смена пароля

    @staticmethod
    def get_not_signed_in_teacher_list():
        teacher_list = session.query(User).filter(User.user_id == 0).all()
        user = []

        for teacher in teacher_list:
            user.append((teacher.id, teacher.teacher))

        return user # Вывод списка учителей для входа
    
    @staticmethod
    def add_event(text, date_time, teacher_id):
        teacher = session.query(User).filter(User.id == teacher_id).first()
        if teacher is None:
            return False # Вывод: учитель не в системе
        
        event = Event(text = text, date_time = date_time, teacher_id = teacher.user_id)
        session.commit()
        session.close()
        return True # Событие добавлено
    
    @staticmethod
    def delete_event(event_id):
        session.query(Event).filter(Event.id == event_id).delete() 
        session.commit()
        session.close() # Удаление события

    @staticmethod
    def get_event_list(teacher_id):
        event_list = session.query(Event).filter(Event.teacher_id == teacher_id).all()
        events = []

        for event in event_list:
            if event.date_time > datetime.now():
                events.append((event.text, event.date_time))

        if events:
            return events # События найдены
        else:
            return False # Нет предстоящих событий