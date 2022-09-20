import os
import requests

class YaUploader:

    def __init__(self, token: str):
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def _upload_link(self, file_path):
        ''' Получить ссылку для загрузки '''
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        params = {"path": file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=self.headers, params=params)
        print(response.status_code)
        return response.json().get("href", "")

    def upload(self, file_path, filename):
        """ Метод загружает файл на яндекс диск """
        path_file = os.path.join(file_path, filename)
        if not os.path.exists(path_file):
            print('upload 25 Некорректный адрес')
            print(path_file)
            return
        # else:
        #     print('upload 29 корректный адрес')

        params = {"path": path_file, "overwrite": "true"}
        href = self._upload_link(file_path=filename)
        if not href:
            print('upload 34 Некорректная ссылка')
            return
        response = requests.put(href,
                                headers=self.headers,
                                params=params,
                                data=open(path_file, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")

class Yadelirium:

    message = ''' Команды:
    p - ввести путь к папке с файлами, которые собираетесь добавлять.
    sp - показать папку с файлами
    a - добавить файл на яндекс диск.
    t - вывести сохраненный токен
    c - показать папку файла конфигурации
    at - изменить токен
    dc - изменить папку файла конфигурации
    i  - info
    q - выход
    '''

    def __init__(self):
        ''' '''
        self.path_token = self._getpathtoken()
        self.tokenfilename = 'dconfig.ini'
        self.token = self._gettoken()
        self.pathfiles = ''
        self.myyadisk = None

    def info(self):
        ''' Можно было так не заморачиваться. '''
        print(self.message)

    def changepathtoken(self):
        ''' команда dc - меняем папку размещения токена '''
        print(f'Текущая папка: {self.path_token}')
        path = input('Введите путь к папке:')

        with open('dsettings.txt', 'w') as f:
            f.write(path)
        self.path_token = path

    def addpath(self):
        ''' команда p - изменяет или добавляет адрес папки с загружаемыми файлами '''
        if self.pathfiles:
            print(f'Текущая папка: {self.pathfiles}')
        path = input('Введите путь к папке:')
        if not os.path.exists(path):
            print('Такой папки не существует.')
        self.pathfiles = path
        print(self.pathfiles)

    def seefilepath(self):
        ''' команда sp - показывает папку с файлами '''
        print(self.pathfiles)

    def addtoken(self):
        ''' команда at - добавляет токен или изменяет сохраненный токен '''
        print(f'Токен будет сохранен в папке по адресу: {self.path_token}')
        if input('Если хотите изменить папку для токена нажвите y:').lower() == 'y':
            self.changepathtoken()
        self.token = input('Введите Ваш токен:')
        if not os.path.exists(self.path_token):
            os.makedirs(self.path_token)
            path_token_file = os.path.join(self.path_token, self.tokenfilename)
            with open(path_token_file, 'wb') as f_token:
                f_token.write(self.token.encode())

    def addfile(self):
        ''' команда a - добавляет файл на яндекс диск '''
        if not self.pathfiles:
            self.addpath()
        filename = input('Введите имя файла:')
        path_file = os.path.join(self.pathfiles, filename)
        if not os.path.exists(path_file):
            print('Некорректный адрес либо такого файла не существует')
            return
        if self.myyadisk is None:
            self.myyadisk = YaUploader(self.token)
        self.myyadisk.upload(self.pathfiles, filename)

    def _gettoken(self):
        ''' достает токен из файла конфига либо возвращает None '''
        path_token_file = os.path.join(self.path_token, self.tokenfilename)
        if os.path.exists(path_token_file):
            with open(path_token_file, 'rb') as f_token:
                token = f_token.read().decode()
            return token

    def _getpathtoken(self):
        ''' достает токен из файла конфига либо возвращает None '''
        if os.path.exists('dsettings.txt'):
            with open('dsettings.txt', 'r') as f:
                path_token = f.read().strip()
            return path_token
        return "C:\Work\configs\\"

    def seetoken(self):
        ''' показывает токен '''
        print(self.token)

    def seepathtoken(self):
        ''' показывает адрес токена '''
        print(self.path_token)

    def menu(self):
        ''' меню команд '''
        self.info()
        comm = ''
        while comm != 'q':
            comm = input('Введите команду:')
            match comm:
                case "p":
                    self.addpath()
                case "sp":
                    self.seefilepath()
                case "a":
                    self.addfile()
                case "t":
                    self.seetoken()
                case "c":
                    self.seepathtoken()
                case "at":
                    self.addtoken()
                case "dc":
                    self.changepathtoken()
                case "i":
                    self.info()
                case _:
                    pass

    def start(self):
        ''' Стартовая функция '''
        if self.token is None:
            self.addtoken()
        else:
            print('Используем сохраненный токен.')
        self.addfile()
        input('Для продолжения нажмите enter')
        self.menu()

    def _testYaUploader(self, path, filename):
        path_file = os.path.join(path, filename)
        print(path_file)
        if not os.path.exists(path_file):
            print('Некорректный адрес либо такого файла не существует')
            return
        myyadisk = YaUploader(self.token)
        myyadisk.upload(path, filename)

    def test(self):

        if self.token is None:
            self.addtoken()
        else:
            print('Используем сохраненный токен.')

        path1 = r'C:\Users\karandash220\Pictures\Осы'
        filename = '1.txt'
        filename2 = 'e873bb77adfd3207ae6fdc9d498be534.jpg'
        self._testYaUploader(path1, filename2)

if __name__ == '__main__':

    yadelirium = Yadelirium()
    yadelirium.start()
    # Если не работает, или запутались в меню, то эта функция проще
    # yadelirium.test()