import json
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from mixer.backend.django import mixer
from ptd.models import Project, ToDo
from ident.models import CustomUser, Organization


# Тестирование с использованием APIClient получения списка заметок
class TestToDo(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Задать данные неизменяемые для всех тестов (админ задается нестандартно)
        CustomUser.objects.create_superuser('admin@admin.com', 'admin123456')

    def setUp(self):
        # Список заметок и проектов, устанавливаемых перед началом каждого теста
        organization = Organization.objects.create(name='Тест mixer')
        user = CustomUser.objects.create(email='masha@ya.ru', password='qwerty12345', organization=organization)
        for i in range(5):  # Создадим 5 проектов
            proj = mixer.blend(Project, users=user)
            for j in range(4):  # По 4 заметки в каждом
                mixer.blend(ToDo, project=proj, user=user)

    def test_to_do_get(self):
        print('Тест чтения списка заметок через REST-API')
        client = APIClient()
        client.login(email='admin@admin.com', password='admin123456')
        response = client.get('/api/todos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # templates = json.loads(response.content)  # получить словарь из json данных для обработки деталей
        self.assertEqual(len(response.data), ToDo.objects.count())

    def test_to_do_put(self):
        print('Тест создания заметки через REST-API')
        client = APIClient()
        client.login(email='admin@admin.com', password='admin123456')
        test_cont = 'Проверочная заметка'
        response = client.post(
            f'/api/todos/',
            {'text_todo': test_cont, 'is_active': 'true', 'user': '1', 'project': '1'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        to_do = ToDo.objects.get(text_todo=test_cont)
        self.assertEqual(to_do.user.email, 'admin@admin.com')
