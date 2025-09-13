from telebot import types, TeleBot
from models import Model

user_states = {}

class Controller:
    def __init__(self, bot):
        self.bot: TeleBot = bot

    def register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            buttons = [
                types.InlineKeyboardButton('Я администратор', callback_data='admin'),
                types.InlineKeyboardButton('Я учитель', callback_data='teacher'),
            ]
            keyboard.add(*buttons)

            self.bot.send_message(message.chat.id, 
                                  f'''Здравствуйте!\n
                                  Выберите свою роль:''', 
                                  reply_markup=keyboard)
            
        @self.bot.callback_query_handler(func=lambda callback: callback.data == 'teacher')
        def teacher(callback):
            pass

        @self.bot.callback_query_handler(func=lambda callback: callback.data == 'admin')
        def admin(callback):
            pass