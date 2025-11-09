from database import get_connection, User, Event, Admin
from sqlalchemy import update
from datetime import datetime
from notifications import Notification

session = get_connection()

class Model:
    @staticmethod
    def add_teacher(teacher_name):
        teacher = User(teacher=teacher_name)
        session.add(teacher)
        session.commit()
        session.close() # Добавление учителя в сисему

    @staticmethod
    def delete_teacher(teacher_id):
        teacher = session.query(User).filter(User.id == teacher_id).first()
        if not teacher:
            return False
        session.query(User).filter(User.id == teacher_id).delete()
        session.query(Event).filter(Event.teacher_id == teacher.id).delete() 
        session.commit()
        session.close() 
        return True # Удаление учителя из системы

    @staticmethod
    def get_teacher(teacher_id):
        teacher = session.query(User).filter(User.id == teacher_id).first()
        return teacher.teacher # Поиск учителя
    
    @staticmethod
    def get_teacher_by_name(teacher):
        teacher = session.query(User).filter(User.teacher == teacher).first()
        return teacher.id # Поиск учителя
    
    @staticmethod
    def sign_in_teacher(teacher_name, user_id): # Вход
        stmt = update(User).where(User.teacher == teacher_name).values(user_id=user_id)
        session.execute(stmt)
        session.commit()
        session.close()

    @staticmethod
    def sign_in_admin(user_id):
        admin = Admin(user_id=user_id)
        session.add(admin)
        session.commit()
        session.close() # Вход в качестве администратора
        
    @staticmethod
    def sign_out_teacher(user_id):
        stmt = update(User).where(User.user_id == user_id).values(user_id = 0)
        session.execute(stmt)
        session.commit()
        session.close() # Выход из системы в главное меню

    @staticmethod
    def sign_out_admin(user_id):
        session.query(Admin).filter(Admin.user_id == user_id).delete()
        session.commit()
        session.close() # Выход из системы в главное меню

    @staticmethod
    def is_it_teacher(user_id):
        user = session.query(User).where(User.user_id == user_id).first()
        
        if user:
            return True # Пользователь - учитель
        else:
            return False # Пользователь не учитель


    @staticmethod
    def is_it_admin(user_id):
        user = session.query(Admin).where(Admin.user_id == user_id).first()

        if user:
            return True # Пользователь - админ
        else:
            return False # Пользователь не админ

    @staticmethod
    def get_not_signed_in_teacher_list():
        teacher_list = session.query(User).filter(User.user_id == 0)
        user = []

        for teacher in teacher_list:
            user.append(teacher.teacher)

        if user:
            return user # Вывод списка учителей для входа
        else:
            return False # Нет профилей для входа
    
    @staticmethod
    def get_signed_in_teacher_list():
        teacher_list = session.query(User).filter(User.user_id != 0).all()

        if teacher_list:
            return teacher_list # Вывод списка вошедших учителей
        else:
            return False # Нет авторизованных учителей
    
    @staticmethod
    def format_datetime_check(date_time):
        format = '%d.%m.%Y %H:%M'

        try:
            parsed_datetime = datetime.strptime(date_time, format)
            return True  # Верный формат
        
        except ValueError:
            return False  # Неверный формат

    @staticmethod
    def add_event(text, date_time_str, teacher_name, admin_id):
        
        format = '%d.%m.%Y %H:%M'
        date_time = datetime.strptime(date_time_str, format)
        
        if teacher_name != 'Для всех':
            teacher = session.query(User).filter(User.teacher == teacher_name).first()

            if teacher:
                event = Event(text=text, date_time_event=date_time, teacher_id=teacher.user_id, admin_id=admin_id)
                session.add(event)
                session.commit()
                
        elif teacher_name == 'Для всех':
            teacher_list = session.query(User).filter(User.user_id != 0).all()
            for teacher in teacher_list:
                event = Event(text=text, date_time_event=date_time, teacher_id=teacher.user_id, admin_id=admin_id)
                session.add(event)
            session.commit()
        
        session.close()
        
    @staticmethod
    def delete_event(event_id):
        session.query(Event).filter(Event.event_id == event_id).delete() 
        session.commit()
        session.close() # Удаление события

    @staticmethod
    def get_event_list(teacher_id):
        event_list = session.query(Event).filter(Event.teacher_id == teacher_id).all()
        events = []

        for event in event_list:
            if event.date_time_event > datetime.now():
                events.append((event.text, event.date_time_event))

        if events:
            return events # События найдены
        else:
            return False # Нет предстоящих событий
    
    @staticmethod
    def get_completed_event(teacher_id):
        event_list = session.query(Event).filter(Event.teacher_id == teacher_id).all()
        events = []

        for event in event_list:
            if event.date_time_event <= datetime.now():
                events.append((event.text, event.date_time_event))

        if events:
            return events # События найдены
        else:
            return False # Нет завершенных событий
        
    @staticmethod
    def presence(event_id, bool):
        stmt = update(Event).where(Event.event_id == event_id).values(presence = bool)
        session.execute(stmt)
        session.commit()
        session.close() # Добавляет присутствие

    @staticmethod
    def get_reason(event_id, text):
        stmt = update(Event).where(Event.event_id == event_id).values(reason = text)
        session.execute(stmt)
        session.commit()
        session.close() # Причина отсутствия

    @staticmethod
    def get_event(event_id):
        event = session.query(Event).filter(Event.id == event_id).first()
        return (event.admin_id, event.text, event.reason) # Сведения о событии