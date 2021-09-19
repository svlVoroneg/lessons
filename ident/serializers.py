from rest_framework.serializers import HyperlinkedModelSerializer
from .models import CustomUser


class CustomUserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'org_id')
