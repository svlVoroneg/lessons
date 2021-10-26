from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer
from .models import Organization, CustomUser
from ptd.serializers import ToDoSerializer


class OrganizationSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        fields = ('name', )


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'organization')


class UserSerializerDocApi(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'organization', 'is_staff', 'is_superuser')
