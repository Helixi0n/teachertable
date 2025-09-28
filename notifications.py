from database import get_connection, User, Event
from telebot import types, TeleBot
from datetime import datetime, timedelta
from time import sleep, time

session = get_connection()

class Notification:
    def __init__(self, bot):
        self.bot: TeleBot = bot

    def send_news(self, text):
            teacher_list = session.query(User).filter(User.user_id != 0).all()
            id_list = []

            for teacher in teacher_list:
                id_list.append(teacher.user_id)

            for id in id_list:
                self.bot.send_message(
                    id, 
                    f'''У вас новая новость:\n
                    {text}'''
                )


    def add_event_notification(self, teacher_id, text, date_time):
        msg = f'Для вас назначено событие:\nНазвание: {text}\nДата и время: {date_time}'
        self.bot.send_message(
             teacher_id,
             msg
        )
                
    def reminder(self):
         while True:
            event_list = session.query(Event).filter(Event.date_time_event).all()
            current_date_time = datetime.now()
            
            for event in event_list:
                event_date = event.date_time_event
                reminder_date_week = event_date - timedelta(days=7)
                reminder_date_day = event_date - timedelta(days=1)

                if current_date_time.date() == reminder_date_week:
                    msg = f'Напоминаем, что через неделю у вас состоится событие "{event.text}"\nДата: {event.date_time_event}'
                    self.bot.send_message(
                        event.teacher_id,
                        msg
                    )
                
                if  current_date_time.date() == reminder_date_day:
                    keyboard = types.InlineKeyboardMarkup(row_width=2)
                    buttons = [
                        types.InlineKeyboardButton('Да', callback_data=f'True_{event.event_id}'),
                        types.InlineKeyboardButton('Нет', callback_data=f'False_{event.event_id}')
                    ]
                    keyboard.add(*buttons)
                    msg = f'Напоминаем, что через день у вас состоится событие "{event.text}"\nДата: {event.date_time_event}\nВы сможете присутствовать?'
                    self.bot.send_message(
                        event.teacher_id,
                        msg,
                        reply_markup=keyboard
                    )

            time.sleep(60)