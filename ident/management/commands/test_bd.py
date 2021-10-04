from django.core.management.base import BaseCommand
from ptd.models import ProjView, Project

class Command(BaseCommand):
    help = 'Тест работы менеджера'

    def handle(self, *args, **kwargs):
         #  ---  Чтение данных   ---
         queryset = Project.objects.all()
         print(queryset)
         print('-----------')
         queryset = ProjView.objects.all()
         print(queryset)
         self.stdout.write(self.style.SQL_KEYWORD('Скрипт завершен.'))
