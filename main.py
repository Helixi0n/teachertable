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
    print("Bot is running...")
    bot.polling()
    threading.Thread(target=notification.reminder).start()