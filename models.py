from database import get_connection, User, Event, Admin, Session
from sqlalchemy import update
from datetime import datetime


class Model:
    @staticmethod
    def add_teacher(teacher_name):
        session = get_connection()
        try:
            teacher = User(teacher=teacher_name)
            session.add(teacher)
            session.commit()
        finally:
            session.close()  # Добавление учителя в систему

    @staticmethod
    def delete_teacher(teacher_id):
        session = get_connection()
        try:
            teacher = session.query(User).filter(User.id == teacher_id).first()
            if not teacher:
                return False
            
            # Сначала удаляем события
            session.query(Event).filter(Event.teacher_id == teacher.id).delete()
            # Затем удаляем учителя
            session.query(User).filter(User.id == teacher_id).delete()
            session.commit()
            return True  # Удаление учителя из системы
        finally:
            session.close()

    @staticmethod
    def get_teacher(teacher_id):
        session = get_connection()
        try:
            teacher = session.query(User).filter(User.id == teacher_id).first()
            return teacher.teacher if teacher else None  # Поиск учителя
        finally:
            session.close()
    
    @staticmethod
    def get_teacher_by_name(teacher_name):
        session = get_connection()
        try:
            teacher = session.query(User).filter(User.teacher == teacher_name).first()
            return teacher.id if teacher else None  # Поиск учителя
        finally:
            session.close()
    
    @staticmethod
    def sign_in_teacher(teacher_name, user_id):  # Вход в профиль учителя
        session = get_connection()
        try:
            stmt = update(User).where(User.teacher == teacher_name).values(user_id=user_id)
            session.execute(stmt)
            session.commit()
        finally:
            session.close()

    @staticmethod
    def sign_in_admin(user_id):  # Вход в профиль администратора
        session = get_connection()
        try:
            admin = Admin(user_id=user_id)
            session.add(admin)
            session.commit()
        finally:
            session.close()
        
    @staticmethod
    def sign_out_teacher(user_id):  # Выход из системы в главное меню
        session = get_connection()
        try:
            stmt = update(User).where(User.user_id == user_id).values(user_id=0)
            session.execute(stmt)
            session.commit()
        finally:
            session.close()

    @staticmethod
    def sign_out_admin(user_id):  # Выход из системы в главное меню
        session = get_connection()
        try:
            session.query(Admin).filter(Admin.user_id == user_id).delete()
            session.commit()
        finally:
            session.close()

    @staticmethod
    def is_it_teacher(user_id):
        session = get_connection()
        try:
            user = session.query(User).filter(User.user_id == user_id).first()
            return user is not None  # Пользователь - учитель
        finally:
            session.close()

    @staticmethod
    def is_it_admin(user_id):
        session = get_connection()
        try:
            user = session.query(Admin).filter(Admin.user_id == user_id).first()
            return user is not None  # Пользователь - админ
        finally:
            session.close()
        
    @staticmethod
    def is_teacher_signed_in(teacher_name):
        session = get_connection()
        try:
            teacher = session.query(User).filter(User.teacher == teacher_name).first()
            if teacher and teacher.user_id != 0:
                return True  # Кто-то зашел в профиль учителя
            else:
                return False  # Профиль учителя свободен
        finally:
            session.close()

    @staticmethod
    def get_not_signed_in_teacher_list():
        session = get_connection()
        try:
            teacher_list = session.query(User).filter(User.user_id == 0).all()
            user = [teacher.teacher for teacher in teacher_list]
            
            if user:
                return user  # Вывод списка учителей для входа
            else:
                return False  # Нет профилей для входа
        finally:
            session.close()
    
    @staticmethod
    def get_signed_in_teacher_list():
        session = get_connection()
        try:
            teacher_list = session.query(User).filter(User.user_id != 0).all()
            
            if teacher_list:
                return teacher_list  # Вывод списка вошедших учителей
            else:
                return False  # Нет авторизованных учителей
        finally:
            session.close()
    
    @staticmethod
    def format_datetime_check(date_time):
        format_str = '%d.%m.%Y %H:%M'

        try:
            datetime.strptime(date_time, format_str)
            return True  # Верный формат
        except ValueError:
            return False  # Неверный формат

    @staticmethod
    def add_event(text, date_time_str, teacher_name, admin_id):
        session = get_connection()
        try:
            format_str = '%d.%m.%Y %H:%M'
            date_time = datetime.strptime(date_time_str, format_str)
            
            if teacher_name != 'Для всех':
                teacher = session.query(User).filter(User.teacher == teacher_name).first()

                if teacher:
                    event = Event(
                        text=text, 
                        date_time_event=date_time, 
                        teacher_id=teacher.id,  # Исправлено: teacher.id вместо teacher.user_id
                        admin_id=admin_id
                    )
                    session.add(event)
                    session.commit()
            else:
                teacher_list = session.query(User).filter(User.user_id != 0).all()
                for teacher in teacher_list:
                    event = Event(
                        text=text, 
                        date_time_event=date_time, 
                        teacher_id=teacher.id,  # Исправлено: teacher.id вместо teacher.user_id
                        admin_id=admin_id
                    )
                    session.add(event)
                session.commit()
        finally:
            session.close()
        
    @staticmethod
    def delete_event(event_id):
        session = get_connection()
        try:
            session.query(Event).filter(Event.event_id == event_id).delete()
            session.commit()  # Удаление события
        finally:
            session.close()

    @staticmethod
    def get_event_list(teacher_id):
        session = get_connection()
        try:
            # Ищем события по ID учителя в таблице User
            teacher = session.query(User).filter(User.user_id == teacher_id).first()
            if not teacher:
                return False
            
            event_list = session.query(Event).filter(Event.teacher_id == teacher.id).all()
            events = []

            for event in event_list:
                if event.date_time_event > datetime.now():
                    events.append((event.text, event.date_time_event))

            if events:
                return events  # События найдены
            else:
                return False  # Нет предстоящих событий
        finally:
            session.close()
    
    @staticmethod
    def get_completed_event(teacher_id):
        session = get_connection()
        try:
            # Ищем события по ID учителя в таблице User
            teacher = session.query(User).filter(User.user_id == teacher_id).first()
            if not teacher:
                return False
            
            event_list = session.query(Event).filter(Event.teacher_id == teacher.id).all()
            events = []

            for event in event_list:
                if event.date_time_event <= datetime.now():
                    events.append((event.text, event.date_time_event))

            if events:
                return events  # События найдены
            else:
                return False  # Нет завершенных событий
        finally:
            session.close()
        
    @staticmethod
    def presence(event_id, bool_val):
        session = get_connection()
        try:
            stmt = update(Event).where(Event.event_id == event_id).values(presence=bool_val)
            session.execute(stmt)
            session.commit()  # Добавляет присутствие
        finally:
            session.close()

    @staticmethod
    def get_reason(event_id, text):
        session = get_connection()
        try:
            stmt = update(Event).where(Event.event_id == event_id).values(reason=text)
            session.execute(stmt)
            session.commit()  # Причина отсутствия
        finally:
            session.close()

    @staticmethod
    def get_event(event_id):
        session = get_connection()
        try:
            event = session.query(Event).filter(Event.event_id == event_id).first()
            if event:
                return (event.admin_id, event.text, event.reason)  # Сведения о событии
            return None
        finally:
            session.close()