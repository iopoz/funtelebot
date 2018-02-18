import datetime
import json

import requests
import configparser

from fun import FunStoryGenerate


class BotHandler:
    def __init__(self, token):
        self.token = token
        self.url = 'https://api.telegram.org/bot%s/' % token

    @property
    def key_board(self):
        key = [{'text': 'FUN'}]
        rkm = {'inline_keyboard': [key]}
        reply = json.dumps(rkm)
        return reply

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.url + method, data=params)
        return resp.json()['result']

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.url + method, data=params)
        return resp

    def send_photo(self, chat_id, photo):
        params = {'chat_id': chat_id, 'photo': photo}
        method = 'sendPhoto'
        resp = requests.post(self.url + method, data=params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()
        if len(get_result) > 0:
            last_update = get_result
        else:
            last_update = None
        return last_update


config = configparser.ConfigParser()
config.read('config.ini')

token = config['DEFAULT']['token']
greet_bot = BotHandler(token)

now = datetime.datetime.now()
fun = FunStoryGenerate()


def main():
    new_offset = None
    today = now.day
    hour = now.hour
    user_dict = {}

    while True:
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()

        if last_update:
            for user in last_update:
                last_update_id = user['update_id']
                last_chat_id = user['message']['chat']['id']
                last_chat_name = user['message']['chat']['first_name']

                if last_chat_id not in user_dict.keys():
                    user_dict[last_chat_id] = today
                    if user_dict[last_chat_id] == now.day and 6 <= hour < 12:
                        greet_bot.send_message(last_chat_id, u'Доброе утро, %s' % last_chat_name)

                    elif user_dict[last_chat_id] == now.day and 12 <= hour < 17:
                        greet_bot.send_message(last_chat_id, u'Добрый день, %s' % last_chat_name)

                    elif today == now.day and 17 <= hour < 23:
                        greet_bot.send_message(last_chat_id, u'Добрый вечер, %s' % last_chat_name)

                fun_res = fun.get_fun()

                greet_bot.send_message(last_chat_id, fun_res)

                new_offset = last_update_id + 1
        if today < now.day:
            user_dict = {}


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
