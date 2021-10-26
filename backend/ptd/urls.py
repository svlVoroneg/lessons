from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from graphene_django.views import GraphQLView

urlpatterns = [
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('openapi', get_schema_view(
        title="Мой проект",
        description="Open API почти без сторонних библиотек (PyYaml требуется)",
        url='http://127.0.0.1:8000/api/',
        version="1.0.0"
    ), name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
]
