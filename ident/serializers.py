from rest_framework.serializers import HyperlinkedModelSerializer
from .models import Organization, CustomUser
from ptd.serializers import ToDoSerializer


class OrganizationSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        fields = ('name', )


class CustomUserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'organization')

    #   Вставка словаря из заметок (в том числе содержит и ссылку на заметки)
    # work = ToDoSerializer(read_only=True, many=True)
