from django_filters import rest_framework as filters
from .models import Project, ToDo


class ToDoFilter(filters.FilterSet):
    #  Дата больше или равно
    from_todo_created = filters.DateTimeFilter(field_name='created', lookup_expr='gte')
    #  Дата меньше или равно
    to_todo_created = filters.DateTimeFilter(field_name='created', lookup_expr='lte')
    #  Выбор из списка пользователей, которые делали заметки
    #  field_name составляется из имени индекса в таблице ТоDo и имени поля в ссылочной таблице
    user_name = filters.AllValuesFilter(field_name='user__first_name')

    class Meta:
        model = ToDo
        fields = ['from_todo_created', 'to_todo_created', 'user_name']


class ProjectFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = Project
        fields = ['name']
