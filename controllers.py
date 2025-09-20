from telebot import types, TeleBot
from models import Model
from notifications import Notification

user_states = {}
admin_states = {}

WRITE_NEWS = 'write news'
ADD_TEACHER = 'add teacher'
ADD_EVENT = 'add event'
ADD_DATE = 'add date'
ADD_TEXT = 'add text'

class Controller:
    def __init__(self, bot):
        self.bot: TeleBot = bot

    def register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            buttons = [
                types.KeyboardButton('Я администратор'),
                types.KeyboardButton('Я учитель')
            ]
            keyboard.add(*buttons)

            self.bot.send_message(
                message.chat.id,           
                f'''Здравствуйте!\n
                Выберите свою роль:''', 
                reply_markup=keyboard
                )
            
        @self.bot.message_handler(func=lambda message: message == 'Назад')
        def main_menu(message):
            if Model.is_it_admin(message.chat.id):
                del admin_states[message.chat.id]
                Model.sign_in_admin(message.chat.id)
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                buttons = [
                    types.KeyboardButton('Добавить учителя'),
                    types.KeyboardButton('Добавить мероприятие'),
                    types.KeyboardButton('Написать новость для учителей'),
                    types.KeyboardButton('Выйти из профиля администратора')
                ]
                keyboard.add(*buttons)

                self.bot.send_message(
                    message.chat.id,
                    'Выберите действие:',
                    reply_markup=keyboard
                )

            elif Model.is_it_teacher(message.chat.id):
                pass

            else:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                buttons = [
                    types.KeyboardButton('Я администратор'),
                    types.KeyboardButton('Я учитель')
                ]
                keyboard.add(*buttons)

                self.bot.send_message(
                    message.chat.id,           
                    'Выберите свою роль:', 
                    reply_markup=keyboard
                    )
                
        @self.bot.message_handler(func=lambda message: message.text == 'Я администратор')
        def admin(message):
            Model.sign_in_admin(message.chat.id)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            buttons = [
                types.KeyboardButton('Добавить учителя'),
                types.KeyboardButton('Добавить мероприятие'),
                types.KeyboardButton('Написать новость для учителей'),
                types.KeyboardButton('Выйти из профиля администратора')
            ]
            keyboard.add(*buttons)

            self.bot.send_message(
                message.chat.id,
                'Выберите действие:',
                reply_markup=keyboard
            )

        @self.bot.message_handler(func=lambda message: message.text == 'Написать новость для учителей')
        def write_news(message):
            if Model.is_it_admin(message.chat.id):
                admin_states[message.chat.id] = WRITE_NEWS
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                keyboard.add(types.KeyboardButton('Назад'))
                self.bot.send_message(
                    message.chat.id,
                    'Напишите текст новости:',
                    reply_markup=keyboard
                )
            else:
                self.bot.send_message(
                    message.chat.id,
                    'Вы не являетесь администратором'
                )

        @self.bot.message_handler(func=lambda message: admin_states.get(message.chat.id) == WRITE_NEWS and message.text != 'Назад')
        def send_news(message):
            news = message.text
            Notification.send_news(news)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            keyboard.add(types.KeyboardButton('Назад'))
            
            self.bot.send_message(
                message.chat.id,
                'Новость разослана',
                reply_markup=keyboard
            )
        
        @self.bot.message_handler(func=lambda message: message == 'Добавить учителя')
        def get_teacher_name(message):
            if Model.is_it_admin(message.chat.id):
                admin_states[message.chat.id] = ADD_TEACHER
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                keyboard.add(types.KeyboardButton('Назад'))

                self.bot.send_message(
                    message.chat.id,
                    'Введите имя учителя:',
                    reply_markup=keyboard
                )
            else:
                self.bot.send_message(
                    message.chat.id,
                    'Вы не являетесь администратором'
                )

        @self.bot.message_handler(func=lambda message: admin_states.get(message.chat.id) == ADD_TEACHER and message.text != 'Назад')
        def add_teacher(message):
            Model.add_teacher(message.text)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            keyboard.add(types.KeyboardButton('Назад'))
            
            self.bot.send_message(
                message.chat.id,
                'Учитель добавлен',
                reply_markup=keyboard
            )


        @self.bot.message_handler(func=lambda message: message.text == 'Я учитель')
        def teacher(message):
            teacher_list = Model.get_not_signed_in_teacher_list()
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            buttons = []

            for key, value in teacher_list.items():
                buttons.append(types.KeyboardButton(value))