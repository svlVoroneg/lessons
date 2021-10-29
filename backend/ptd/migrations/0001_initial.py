# Generated by Django 3.2.7 on 2021-10-06 07:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Наименование проекта')),
                ('repo', models.URLField(blank=True, verbose_name='Ссылка на репозиторий')),
            ],
            options={
                'verbose_name': 'Проект(просмотр)',
                'verbose_name_plural': 'Проекты(просмотр)',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Наименование проекта')),
                ('repo', models.URLField(blank=True, verbose_name='Ссылка на репозиторий')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Проект',
                'verbose_name_plural': 'Проекты',
            },
        ),
        migrations.CreateModel(
            name='ToDo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_todo', models.TextField(verbose_name='Текст заметки')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('is_active', models.BooleanField(default=True, verbose_name='Признак активности заявки')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='note', to='ptd.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='work', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Заметка',
                'verbose_name_plural': 'Заметки',
            },
        ),
    ]