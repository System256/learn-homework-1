"""
Домашнее задание №1

Использование библиотек: ephem

* Установите модуль ephem
* Добавьте в бота команду /planet, которая будет принимать на вход
  название планеты на английском, например /planet Mars
* В функции-обработчике команды из update.message.text получите
  название планеты (подсказка: используйте .split())
* При помощи условного оператора if и ephem.constellation научите
  бота отвечать, в каком созвездии сегодня находится планета.

"""
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import ephem
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')


def greet_user(update, context):
    text = 'Вызван /start'
    print(text)
    user_name = update.message.chat.first_name
    update.message.reply_text(
        f"Здравствуй, {user_name}")
    

def name_planet(update, context):
    planet_name = update.message.text.split()[-1].capitalize()
    if planet_name in [name for _0, _1, name in ephem._libastro.builtin_planets()]:
        if hasattr(ephem, planet_name):
            planet = getattr(ephem, planet_name)(datetime.now())
            update.message.reply_text(f"Планета {planet_name} находится сегодня в созвездии {ephem.constellation(planet)[-1]}")
        else:
            update.message.reply_text(f"Планеты {planet_name} не существует.")


def talk_to_me(update, context):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)


def main():
    mybot = Updater(os.environ['TOKEN'])

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", name_planet))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info("Бот запущен")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
