from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin, ListModelMixin
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from .models import Project, ToDo
from .serializers import ProjectSerializer, ToDoSerializer
from .filters import ProjectFilter, ToDoFilter


class ProjectLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10


class ProjectViewSet(ModelViewSet):
    # Переопределение рендера в классе приоритет перед глобальными настройками
    # renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = ProjectLimitOffsetPagination
    filterset_class = ProjectFilter


class ToDoLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20


#  Решил пойти по пути написания минимума кода и переопределил две операции
class ToDoView(GenericViewSet, ListModelMixin,  UpdateModelMixin, CreateModelMixin):
    queryset = ToDo.objects.all().filter(is_active=True)
    #  Работает с ModelSerializer не работает с HyperlinkedModelSerializer
    serializer_class = ToDoSerializer
    pagination_class = ToDoLimitOffsetPagination
    filterset_class = ToDoFilter

    def destroy(self, request, *args, **kwargs):
        #  заменяем удаление на обновление записи
        instance = self.get_object()
        instance.is_active = False
        instance.save(update_fields=['is_active'])
        #  не уверен, что правмльно, но ответ сохранил как в destroy
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_active:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else: return Response(status=status.HTTP_404_NOT_FOUND)
