from rest_framework.serializers import HyperlinkedModelSerializer
from .models import Organization, CustomUser


class OrganizationSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        fields = ('name', )


class CustomUserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'org_id')
