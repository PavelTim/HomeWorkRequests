import requests
import os
import json
from pprint import pprint
''' Задание 1. Кто самый умный? '''

def test_request(method='/all.json'):
    ''' Запрос по всем данным по всем супергероям - чтобы не мучиться '''
    url = "https://akabab.github.io/superhero-api/api" + method
    response = requests.get(url)

    if response.status_code == 200:
        print('request is OK')
    else:
        print('ERROR', response.status_code)
        return
    return response.json()


def hulk_thanos_captain(response):
    ''' Задание 1. Кто умнее Таноса? '''
    d = {}
    for i in response:
        if i['name'] == 'Thanos':
            d['Thanos'] = i['powerstats']['intelligence']
        elif i['name'] == 'Hulk':
            d['Hulk'] = i['powerstats']['intelligence']
        elif i['name'] == 'Captain America':
            d['Captain America'] = i['powerstats']['intelligence']
        elif len(d) == 3:
            break

    print('Искомые герои:')
    for key, value in d.items():
        print(f'{key}, его интеллект равен {value}')
    print('Самый умный из этих трех, естесственно:')
    cleverest = sorted(d, key=lambda x: d[x])[-1]
    print(cleverest)
    print('Непонятно, зачем ему, при таком интеллекте, заниматься столь примитивной демографической политикой?')

def main():
    ''' '''
    path = "datahero.json"
    if not os.path.exists(path):
        print('Данные не сохранены. Делаем запрос и сохраняем результаты в файл.')
        response = test_request()
        with open(path, 'w') as f:
            json.dump(response, f)
    else:
        print('Файл существует. Берем результаты запроса, сохраненные в файле, не делая запрос.')
        with open(path) as f:
            response = json.load(f)

    hulk_thanos_captain(response)


if __name__ == '__main__':
    main()
    # response = test_request()
    # pprint(response.json())

