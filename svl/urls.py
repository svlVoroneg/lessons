from django.contrib import admin
from django.urls import path, include, re_path
# Rest API
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
# Создание документации Open API
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
# Кастомные настройки
from ident.views import CustomUserView, OrganizationViewSet, UserListAPIView, UserView
from ptd.views import ProjectViewSet, ToDoView

# Создание Url Для REST API
router = DefaultRouter()
router.register('users', CustomUserView, basename='users')
router.register('projects', ProjectViewSet, basename='projects')
router.register('todos', ToDoView, basename='todos')
# Добавляем версионированные выводы для пользователя
router.register('usersv', UserView, basename='usersv')
#  Дополнение моей модели
router.register('org', OrganizationViewSet)

# Представление для схемы OpenAPI
schema_view = get_schema_view(
    openapi.Info(
        title="OpenAPI для проекта Заметки",
        default_version='2.0',
        description="Документация по учебному проекту",
        contact=openapi.Contact(email="admin@admin.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Номер версии API передается в заголовке URL пример: http://127.0.0.1:8000/api/users/ или
    # Номер версии API передается в параметре URL пример: http://127.0.0.1:8000/api/users/?version=1.0
    # в этих случаях можно использовать стандартный роутер (как и для безверсионного API)
    # (для остальных вариантов версионности API его надо закомментировать)
    path('api/', include(router.urls)),
    # Варианты задания номера версии (менять синхронно с settings.py)
    # Номер версии API передается в URL пример: http://127.0.0.1:8000/api/2.0/users/
    # re_path(r'^api/(?P<version>\d\.\d)/users/$', UserListAPIView.as_view()),
    #  Номер версии API передается в URL пример: http://127.0.0.1:8000/api/users/v1
    # path('api/users/v1', include('ident.urls', namespace='1.0')),
    # path('api/users/v2', include('ident.urls', namespace='2.0')),
    # --------- конец блока url, связанных с версионностью API

    # url документации на API
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    #  url для функционирования визуального интерфейса API
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token),
    #  "обычный" сайт
    path('', include('ident.urls')),
    path('', include('ptd.urls')),
]
