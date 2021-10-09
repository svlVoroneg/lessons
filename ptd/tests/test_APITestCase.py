import json
from rest_framework.test import APITestCase
from rest_framework import status
from mixer.backend.django import mixer
from ptd.models import Project, ToDo
from ident.models import CustomUser, Organization
from ptd.views import ProjectSerializer, ToDoSerializer
from ident.views import CustomUserSerializer, OrganizationSerializer


# Тестирование с использованием APITestCase
class TestViewSet(APITestCase):
    #  T.к. mixer не осилил мою модель - залил подготовленную базу из json
    # создание файла json из текущей базы:
    # python manage.py dumpdata -o test.json --i 1 -e ptd.projview -e contenttypes -e admin.logentry
    # после этого преобразовать файл в кодировку utf-8 (иначе ругается на русские буквы)
    fixtures = ['test.json', ]

    def setUp(self):
        # Действия, выполняемые перед началом каждого теста
        # паролей существующих пользователей не помним, создаем допролнительного суперюзера
        CustomUser.objects.create_superuser('admin@admin.com', 'admin123456')
        self.client.login(email='admin@admin.com', password='admin123456')

    def test_get_list(self):
        print('Тест REST-API получение списка пользователей')
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_count = CustomUser.objects.count()
        # сравним, что количество считаных пользователей равно имеющимся в базе
        self.assertEqual(len(response.data), user_count)

    def test_project_api(self):
        print('Тест REST-API созданние и удаление проекта')
        old_proj = Project.objects.count()
        user = CustomUser.objects.get(email='admin@admin.com')
        # Создадим новый проект от созданного суперюзера и от начального
        response = self.client.post(
            f'/api/projects/',
            {'name': 'Тест теста удаления', 'repo': '', 'users': ['1', user.id]})
        # проверим корректность полученного кода возврата
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Получим ответ в виде словаря - по ключу id получим id созданной записи в БД
        template = json.loads(response.content)
        proj_id = template['id']
        # Посчитаем новое кол-во проектов в базе - должно увеличиться на 1
        self.assertEqual(old_proj+1, Project.objects.count())
        response = self.client.delete(f'/api/projects/{proj_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # После удаления снова посчитаем проекты - кол-во должно вернуться к начальному
        self.assertEqual(old_proj, Project.objects.count())

    def test_how_del_todo(self):
        print('Тест REST-API удаление заметки')
        kol_todo = ToDo.objects.count()
        # Проверка не удаления существующей заметки через delete
        to_do = ToDo.objects.first()
        response = self.client.delete(f'/api/todos/{to_do.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # После удаления снова посчитаем заметки - кол-во не должно измениться
        self.assertEqual(kol_todo, ToDo.objects.count())
        # Теперь проверим удаление путем изменения свойства is_active
        response = self.client.put(
            f'/api/todos/{to_do.id}/',
            {'text_todo': to_do.text_todo, 'is_active': 'false', 'user': to_do.user_id, 'project': to_do.project_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # После изменения снова посчитаем заметки - кол-во должно уменьшится на 1
        self.assertEqual(kol_todo, ToDo.objects.count()+1)
