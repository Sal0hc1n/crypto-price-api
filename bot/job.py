from bot.App import bot
from bot import crud
from bot import coin


def user_job(chat_id):
    user = crud.get_user(chat_id)

    new_value = coin.get_current_value()
    diff = new_value - user.value
    if abs(diff) > user.overweight:
        crud.update_value(chat_id, new_value)
        prefix = "Up" if diff > 0 else "Down"
        body = prefix + ": " + str(new_value) + " | Diff: " + str(int(diff))
        bot.send_message(chat_id, body)
    if new_value > user.max_value:
        body = "Alert! Rose higher: " + str(user.max_value) + " | " + " Current: " + str(new_value)
        crud.update_max_value(chat_id, new_value)
        bot.send_message(chat_id, body)
    if new_value < user.min_value:
        body = "Alert! Fell below: " + str(user.min_value) + " | " + " Current: " + str(new_value)
        crud.update_min_value(chat_id, new_value)
        bot.send_message(chat_id, body)
