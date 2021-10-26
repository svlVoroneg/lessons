"""
Данный тест не создает и не удаляет базу данных, а работает с существующей
для корректного прохождения параллельно должен быть запущен web сервер
осуществляется тестирование его API
Начальное заполнение БД (если не выполнялось) осуществляется командой
python manage.py init.user
!!!!
Не может запускаться одновременно со стандартными тестами Django,
если используется development сервер Django (python manage.py runserver)
временно пометил как незапускаемый
"""
import json
import unittest
import requests
from ptd.models import Project, ToDo
from ident.models import CustomUser, Organization


class SimpleTest(unittest.TestCase):
    token = {}

    def setUp(self):
        # Действия, выполняемые перед началом каждого теста - получение токена авторизации
        response = requests.post('http://127.0.0.1:8000/api-token-auth/', json={
            'username': 'svl@35r.ru',
            'password': 'Zaq12wsx'})
        assert response.status_code == 200
        answer = json.loads(response.content)
        self.token = {'Authorization': 'Token ' + answer['token']}

    def test_list_user(self):
        print('Live Тест Get на REST-API с использованием токена')
        response = requests.get('http://127.0.0.1:8000/api/users/', headers=self.token)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == CustomUser.objects.count()

    def test_add_project(self):
        print('Live Тест Post на REST-API с использованием токена')
        proj_name = 'Тест создания проекта через API'
        response = requests.post('http://127.0.0.1:8000/api/projects/', json={
            'name': proj_name, 'repo': '', 'users': ['1', ]
        }, headers=self.token)
        assert response.status_code == 201
        proj_id = json.loads(response.content)['id']
        proj = Project.objects.get(pk=proj_id)
        assert proj.name == proj_name
        proj.delete()  # Удалим созданную тестовую запись / приведение к начальному состоянию
