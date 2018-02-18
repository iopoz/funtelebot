import random

import requests


class FunStoryGenerate:
    def __init__(self):
        self.url_list = {'https://ultragenerator.com/anekdotov/handler.php': {},
                         'http://freegenerator.ru/shutok': {'type': 'shutok'}}


    def get_fun(self):
        url, data_req = random.choice(list(self.url_list.items()))#self.url_list[randint(0, len(self.url_list) - 1)]
        response = requests.post(url, data=data_req)
        try:
            res = response.json()
            res = res['text']
            #img = None
        except:
            res = response.text
            res = res.replace('<br />', '')
            #img = res[res.find('<'):]
            res = res[0: res.find('<')]
            # img_url = img.split('"')
            # img = img_url[1]
        return res #dict(fun_text=res, fun_image=img)