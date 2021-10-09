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
        # заодно проверим работу mixer со сложными связями между таблицами
        # to_do = mixer.blend(ToDo)  # - такая конструкция не заработала
        # proj = mixer.blend(Project) - такая тоже
        user = CustomUser.objects.get(pk=1)
        proj = Project(name='Тест теста', repo='')
        proj.save()
        proj.users.add(user)
        ToDo.objects.create(project=proj, text_todo='Тест теста', is_active=True, user=user)
        ToDo.objects.create(project=proj, text_todo='Вторая заметка', is_active=True, user=user)

    def test_to_do_get(self):
        print('Тест чтения списка из двух заметок через REST-API')
        client = APIClient()
        client.login(email='admin@admin.com', password='admin123456')
        response = client.get('/api/todos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # templates = json.loads(response.content)  # получить массив json данных для обработки деталей
        self.assertEqual(len(response.data), 2)

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
