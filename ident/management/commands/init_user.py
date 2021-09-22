from ident.models import CustomUser, Organization
from django.core.management.base import BaseCommand
import json


class Command(BaseCommand):
    help = 'Инициализация пользователей'

    def add_arguments(self, parser):
        #  Позиционные аргументы
        parser.add_argument('EmailSU', type=str, help='E-mail суперпользователя', default='svl@35r.ru')
        parser.add_argument('PassSU', type=str, help='Пароль суперпользователя', default='Zaq12wsx')
        #  Опциональные аргументы
        parser.add_argument(
            '-f', '--file', type=str,
            help='Файл с json описанием пользователей',
            default='spisuser.json')

    def handle(self, *args, **kwargs):
        #  Получение значений аргументов
        email_su = kwargs['EmailSU']
        pass_su = kwargs['PassSU']
        file_us = kwargs['file']
        #  ---  Создание суперпользователя  ---
        CustomUser.objects.create_superuser(email=email_su, password=pass_su)
        self.stdout.write(self.style.SUCCESS('Создан суперпользователь'))
        #   ---  Создание пользователей из json файла  ---
        with open(file_us, 'r', encoding='utf-8') as f:
            templates = json.load(f)
        # создадим организацию, если необходимо
        try:
            org = Organization.objects.get(name=templates['NameOrg'])
        except Organization.DoesNotExist:
            org = Organization(name=templates['NameOrg'])
            org.save()
        #  список пользователей организации
        spis_user = templates['users']
        for us in spis_user:
            CustomUser.objects.create_user(
                email=us['email'],
                password=us['password'],
                оrganization=org.pk,
                first_name=us['firstName'],
                last_name=us['lastName'])
            self.stdout.write(self.style.SQL_COLTYPE('Создан тестовый пользователь ' + us['email']))
        self.stdout.write(self.style.SQL_KEYWORD('Скрипт завершен.'))
