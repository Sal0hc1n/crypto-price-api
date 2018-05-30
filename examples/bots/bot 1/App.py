# -*- coding: utf-8 -*-
from bot.config import AppConfig
import telebot
from bot import crud, scheduler
from bot import help
from bot import coin


bot = telebot.TeleBot(AppConfig.token)


@bot.message_handler(commands=["help"])
def help_command(message):
    bot.send_message(message.chat.id, help.help_text(message.chat.id))


@bot.message_handler(commands=["overweight"])
def change_overweight(message):
    args = message.text.split()
    overweight = args[1] if 1 < len(args) else None
    if overweight and overweight.isdigit():
        crud.update_overweight(message.chat.id, overweight)
    else:
        bot.send_message(message.chat.id, help.overweight_text)


@bot.message_handler(commands=["interval"])
def change_interval(message):
    args = message.text.split()
    interval = args[1] if 1 < len(args) else None
    if interval and interval.isdigit():
        crud.update_interval(message.chat.id, interval)
        user = crud.get_user(message.chat.id)
        if user.run:
            scheduler.remove_job(message.chat.id)
            scheduler.add_job(message.chat.id)
    else:
        bot.send_message(message.chat.id, help.interval_text)


# @bot.message_handler(commands=["diff"])
# def change_diff(message):
#     args = message.text.split()
#     diff = args[1] if 1 < len(args) else None
#     if diff and diff.isdigit():
#         crud.update_diff(message.chat.id, diff)
#     else:
#         bot.send_message(message.chat.id, help.diff_text)


@bot.message_handler(commands=["min_value"])
def change_min_value(message):
    args = message.text.split()
    min_value = args[1] if 1 < len(args) else None
    if min_value and min_value.isdigit():
        crud.update_min_value(message.chat.id, min_value)
    else:
        bot.send_message(message.chat.id, help.min_value_text)


@bot.message_handler(commands=["max_value"])
def change_max_value(message):
    args = message.text.split()
    max_value = args[1] if 1 < len(args) else None
    if max_value and max_value.isdigit():
        crud.update_max_value(message.chat.id, max_value)
    else:
        bot.send_message(message.chat.id, help.max_value_text)


@bot.message_handler(commands=["run"])
def run(message):
    current_value = coin.get_current_value()
    bot.send_message(message.chat.id, "Current value: "+str(current_value))
    scheduler.add_job(message.chat.id)


@bot.message_handler(commands=["stop"])
def stop(message):
    scheduler.remove_job(message.chat.id)


@bot.message_handler(commands=["start"])
def start(message):
    crud.create_user(message.chat.id)
    bot.send_message(message.chat.id, help.help_text(message.chat.id))


@bot.message_handler(commands=["current"])
def current(message):
    current_value = coin.get_current_value()
    bot.send_message(message.chat.id, current_value)


if __name__ == '__main__':
    crud.clear_users()
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            pass
