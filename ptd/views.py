from rest_framework.viewsets import ModelViewSet
from .models import Project, ToDo
from .serializers import ProjectSerializer, ToDoSerializer, HyperlinkedProjectSerializer


class ProjectViewSet(ModelViewSet):
    # Переопределение рендера в классе приоритет перед глобальными настройками
    # renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class HyperlinkedProjectViewSet(ModelViewSet):
    # Переопределение рендера в классе приоритет перед глобальными настройками
    # renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    queryset = Project.objects.all()
    serializer_class = HyperlinkedProjectSerializer


class ToDoViewSet(ModelViewSet):
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer
