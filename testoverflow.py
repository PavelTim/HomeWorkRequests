import requests
import json
import os
from pprint import pprint
from time import sleep
import datetime as dd


class MyStackExchangeRequests:
    BASE_URL = 'https://api.stackexchange.com/2.3'
    QUESTIONS = '/questions'
    URL_QUESTIONS = 'https://api.stackexchange.com/2.3/questions'

    def __init__(self, order='desc', sort="activity", site="stackoverflow"):

        self.params = {
            "order": order,
            "sort": sort,
            "site": site
        }

    def period(self, period):
        ''' Получаем период в днях в виде двух дат в требуемом формате (в секундах с начала эпохи)'''
        now = dd.datetime.now()
        todate = int(dd.datetime.timestamp(now))
        fromdate = int(dd.datetime.timestamp(now - dd.timedelta(days=period)))
        return {'todate': todate, 'fromdate': fromdate}

    def get_questions(self, tag, period=2):
        ''' Запрос вопросов '''

        params = {**self.params, **self.period(period)}
        params['tagged'] = tag
        print('get_questions:', params)
        response = requests.get(self.URL_QUESTIONS, params=params)
        print(response.status_code)
        response.raise_for_status()
        return response.json()

if __name__ == '__main__':

    if os.path.exists('dresponse.json'):
        with open('dresponse.json', 'r') as f:
            res = json.load(f)
        print('Сохраненный запрос')
    else:
        myoverflow = MyStackExchangeRequests()
        res = myoverflow.get_questions_by_tag('python')
        with open('dresponse.json', 'w') as f:
            json.dump(res, f)
    print('Длина запроса:', len(res))
    print('Заголовки:', *(key for key in res))
    any(print(f'{key}:', value) for key, value in res.items() if key != 'items')
    print(len(res['items']))
    for item in res['items'][:3]:
        pprint(item)
    item_0 = res['items'][0]
    print()
    sleep(0.1)
    print('Заголовки:', *(key for key in item_0), sep='\n')