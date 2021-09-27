from django.core.management.base import BaseCommand
from ptd.models import ToDo

class Command(BaseCommand):
    help = 'Тест работы менеджера'

    def handle(self, *args, **kwargs):
         #  ---  Чтение данных   ---
        queryset = ToDo.active_todo.all()
        print(queryset)
        self.stdout.write(self.style.SQL_KEYWORD('Скрипт завершен.'))
