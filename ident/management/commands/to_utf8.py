from django.core.management.base import BaseCommand
from ptd.models import ProjView, Project
import json


class Command(BaseCommand):
    help = 'Преобразование русских букв в многобайтовую кодировку UTF-8'

    def add_arguments(self, parser):
        parser.add_argument(
            '-i', '--input', type=str,
            help='Файл json c русскими символами',
            default='test.json')
        parser.add_argument(
            '-o', '--output', type=str,
            help='Преобразованный Файл json',
            default='test_utf8.json')

    def handle(self, *args, **kwargs):
        #  Получение значений аргументов
        file_input = kwargs['input']
        file_output = kwargs['output']
        # обработаем файл построчно
        with open(file_output, 'wb') as itog:
            with open(file_input, 'r', encoding='utf-8') as f:
                line = f.readline()
                while line:
                    tekst = line.encode('utf-8')
                    itog.write(tekst)
                    line = f.readline()
