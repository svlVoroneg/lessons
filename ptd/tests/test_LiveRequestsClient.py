import json
from rest_framework import status
from rest_framework.test import RequestsClient, CoreAPIClient, APITestCase
from ptd.models import Project, ToDo
from ident.models import CustomUser, Organization
from ptd.views import ProjectViewSet
from mixer.backend.django import mixer



class RequestsClientTests(APITestCase):
    token = {}

    @classmethod  # Задать данные неизменяемые для всех тестов
    def setUpTestData(cls):
        CustomUser.objects.create_superuser('admin@admin.com', 'admin123456')
        organization = Organization.objects.create(name='Тест mixer')
        user = CustomUser.objects.create(email='masha@ya.ru', password='qwerty12345', organization=organization)
        for i in range(4):  # Создадим 4 проекта
            proj = mixer.blend(Project, users=user)
            for j in range(i):  # количество заметок в каждом проекте равно номеру проекта
                mixer.blend(ToDo, project=proj, user=user)

    def setUp(self):
        # Действия, выполняемые перед началом каждого теста - получение токена авторизации
        self.client = RequestsClient()
        response = self.client.post('http://127.0.0.1:8000/api-token-auth/', json={
            'username': 'admin@admin.com',
            'password': 'admin123456'})
        assert response.status_code == 200
        answer = json.loads(response.content)
        self.token = {'Authorization': 'Token ' + answer['token']}

    def test_auth_user(self):
        print('Live Тест Get на REST-API с использованием токена')
        response = self.client.get('http://127.0.0.1:8000/api/users/', headers=self.token)
        assert response.status_code == 200
        # тот-же запрос на адрес по умолчанию (можно использовать любой из адресов)
        response = self.client.get('http://testserver/api/users/', headers=self.token)
        assert response.status_code == status.HTTP_200_OK

    def test_progjects(self):
        print('Live Тест Post на REST-API с использованием токена')
        proj_name = 'Тест создания project'
        response = self.client.post('http://testserver/api/projects/', json={
            'name': proj_name, 'repo': '', 'users': ['1',]
        }, headers=self.token)
        assert response.status_code == status.HTTP_201_CREATED
        proj_id = json.loads(response.content)['id']
        proj = Project.objects.get(pk=proj_id)
        assert proj.name == proj_name
