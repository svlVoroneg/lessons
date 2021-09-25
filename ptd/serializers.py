from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer
from rest_framework import serializers
from .models import Project, ToDo


class ToDoSerializer(ModelSerializer):
    class Meta:
        model = ToDo
        fields = '__all__'


# Для пользователей, работающих с проектом будут сгенерированы pk
class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
#   Вставка ссылок на заметки
#    note = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='todo-detail')
#   Вставка словаря из заметок (в том числе содержит и ссылку на заметки)
    note = ToDoSerializer(read_only=True, many=True)


'''  Блок примеров разного вида сериализаторов (урок 3)
# Варианты, работаюшие с HyperlinkedModelSerializer (5):
# Для пользователей, работающих с проектом будут сгенерированы гиперссылки
class HyperlinkedProjectSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
#  2 Вставка описаний из строкового представления модели заметок
#    note = serializers.StringRelatedField(many=True, read_only=True)
#  3 Вставка первичных ключей модели заметок
#    note = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#  4 Вставка только одного поля из модели заметок
#    note = serializers.SlugRelatedField(read_only=True, many=True, slug_field='text_todo')
#  5 Вставка ссылок на заметки
    note = serializers.HyperlinkedIdentityField(read_only=True, many=True, view_name='todo-detail')
'''
