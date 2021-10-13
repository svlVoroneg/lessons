import requests
import json
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Тест: версия API передается в заголовке URL (требуется запущенный Web сервер)'

    def handle(self, *args, **kwargs):
        response = requests.post('http://127.0.0.1:8000/api-token-auth/', json={
            'username': 'svl@35r.ru',
            'password': 'Zaq12wsx'})
        answer = json.loads(response.content)
        token = 'Token ' + answer['token']
        response = requests.get(
            'http://127.0.0.1:8000/api/usersv/',
            headers={'Authorization': token})
        print('Версия API по умолчанию')
        print(json.loads(response.content))
        response = requests.get(
            'http://127.0.0.1:8000/api/usersv/',
            headers={'Accept': 'application/json; version=1.0', 'Authorization': token})
        print('Версия API 1.0')
        print(json.loads(response.content))
