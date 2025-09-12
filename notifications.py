from database import get_connection, User
from telebot import types, TeleBot

session = get_connection()

class Notification:
    def __init__(self, bot):
        self.bot: TeleBot = bot

    def notifications(self):
        @staticmethod
        def send_news(text):
            teacher_list = session.query(User).all()
            id_list = []

            for teacher in teacher_list:
                id_list.append(teacher.user_id)

            for id in id_list:
                self.bot.send_message(id, 
                                      f'''У вас новая новость:\n
                                      {text}''')
                
        @staticmethod
        def reminder_week():
            pass

        @staticmethod
        def reminder_day():
            pass