from telebot import TeleBot
from controllers import Controller
from notifications import Notification
from constants import TOKEN

# Главный файл, запустить для начала работы бота

bot = TeleBot(TOKEN)
controller = Controller(bot)
notification = Notification(bot)

controller.register_handlers()
notification.notifications()

if __name__ == "__main__":
    print("Bot is running...")
    bot.polling()