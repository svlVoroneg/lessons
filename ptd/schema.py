from graphene_django import DjangoObjectType
import graphene
from .models import Project, ToDo
from ident.models import CustomUser, Organization
from .filters import ProjectFilter


class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = '__all__'


class ToDoType(DjangoObjectType):
    class Meta:
        model = ToDo
        fields = '__all__'


class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = '__all__'


class Query(graphene.ObjectType):
    all_projects = graphene.List(ProjectType)
    all_to_dos = graphene.List(ToDoType)
    all_users = graphene.List(UserType)
    project_srch = graphene.List(ProjectType, name=graphene.String())

    def resolve_all_projects(self, info):
        return Project.objects.all()

    def resolve_all_to_do(self, info):
        return Project.objects.all()

    def resolve_all_user(self, info):
        return CustomUser.objects.all()

    #  Фильтрация проектов по содержанию поля название
    def resolve_project_srch(self, info, name):
        try:
            return Project.objects.filter(name__contains=name)
        except Project.DoesNotExist:
            return None


schema = graphene.Schema(query=Query)

'''
Вызов списка проектов с подсписками пользователей и заметок проекта
Обращение к таблице заметок идет по related_name поля в модели 
{
  allProjects{
    id
    name
    users{
      id
      firstName
    }
    note{
      id
      textTodo
    }
  }
}
'''
