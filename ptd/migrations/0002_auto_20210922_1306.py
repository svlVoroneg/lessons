# Generated by Django 3.2.7 on 2021-09-22 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ptd', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todo',
            old_name='proj_id',
            new_name='project',
        ),
        migrations.RenameField(
            model_name='todo',
            old_name='user',
            new_name='users',
        ),
    ]
