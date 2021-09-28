from django.db import models
import ident.models


class Project(models.Model):
    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    name = models.CharField(max_length=64, verbose_name='Наименование проекта', unique=True)
    repo = models.URLField(verbose_name='Ссылка на репозиторий', blank=True)
    users = models.ManyToManyField(ident.models.CustomUser)

    def __str__(self):
        return self.name


class ToDoActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class ToDo(models.Model):
    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='note')
    text_todo = models.TextField(verbose_name='Текст заметки')
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    modified = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    is_active = models.BooleanField(verbose_name='Признак активности заявки', default=True)
    user = models.ForeignKey(ident.models.CustomUser, on_delete=models.PROTECT)
    #  Переопределение возвращаемого результата - только активные заметки
    objects = ToDoActiveManager()
    # сохранение  стандартного менеджера (для реализации возможности восстановления заметок)
    # порядок определения важен, если поставить первым стандартный менеджер, то фильтрация
    # применится только к заметкам ToDo
    all_objects = models.Manager()



    def __str__(self):
        return f'{self.text_todo} {self.created} {self.is_active}'
