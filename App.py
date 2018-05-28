from exchanges.coinapult import Coinapult
from twilio.rest import Client
from config import AppConfig
import time
import os.path

tclient = Client(AppConfig.account_sid, AppConfig.auth_token)
old_value = 0
min_value = 0
max_value = 0


def write_to_file(value):
    if not os.path.isfile(AppConfig.res_file):
        open(AppConfig.res_file, 'a').close()
    with open(AppConfig.res_file, 'r') as fin:
        data = fin.read().splitlines(True)
        if len(data) == AppConfig.file_len:
            with open(AppConfig.res_file, 'w') as fout:
                fout.writelines(data[1:])
    with open(AppConfig.res_file, 'a') as file:
        file.write(str(value) + '\n')


def send_message(body_message):
    for to in AppConfig.to_:
        tclient.messages.create(
            to,
            from_=AppConfig.from_,
            body=body_message)
        time.sleep(1)


while True:
    new_value = Coinapult().get_current_price()
    write_to_file(new_value)
    diff = new_value - old_value
    if abs(diff) > AppConfig.odds:
        old_value = new_value
        prefix = "Up" if diff > 0 else "Down"
        body = prefix+": "+str(new_value)+" | Diff: "+str(diff)
        send_message(body)
    if new_value > max_value:
        body = "Alert! Rose higher: "+str(max_value)+" | "+" Current: "+str(new_value)
        max_value += AppConfig.diff
        send_message(body)
    if new_value < min_value:
        body = "Alert! Fell below: "+str(min_value)+" | "+" Current: "+str(new_value)
        min_value -= AppConfig.diff
        send_message(body)
    time.sleep(AppConfig.interval)
