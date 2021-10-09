from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from ptd.models import Project, ToDo
from ident.models import CustomUser, Organization
from ptd.views import ProjectViewSet


# Тестирование авторизации с использованием APIRequestFactory
class TestProjectViewSet(TestCase):

    def setUp(self):
        # Список пользователей, создаваемых перед началом каждого теста
        CustomUser.objects.create_superuser('admin@admin.com', 'admin123456')

    def test_get_list(self):
        print('Проверка Не получения списка проектов не авторизованым пользователем')
        factory = APIRequestFactory()
        request = factory.get('/api/projects/')
        view = ProjectViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list_auth(self):
        print('Проверка получения списка проектов суперпользователем')
        factory = APIRequestFactory()
        request = factory.get('/api/projects/')
        admin = CustomUser.objects.get(pk=1)
        force_authenticate(request, admin)
        view = ProjectViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
