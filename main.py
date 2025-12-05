from telebot import TeleBot
from controllers import Controller
from notifications import Notification
import threading
from constants import TOKEN

# Главный файл, запустить для начала работы бота

bot = TeleBot(TOKEN)
controller = Controller(bot)
notification = Notification(bot)

controller.register_handlers()

if __name__ == "__main__":
    try:
        print("Bot is running...")

        reminder_thread = threading.Thread(target=notification.reminder)
        reminder_thread.daemon = True
        reminder_thread.start()

        bot.polling(none_stop=True)
    except Exception as e:
        print(f'Ошибка: {e}')