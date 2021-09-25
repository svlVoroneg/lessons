from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from .models import Organization, CustomUser
from .serializers import OrganizationSerializer, CustomUserSerializer
# импорты для формы
from .forms import CustomUserForm
from django.shortcuts import render
from django.http import HttpResponse


class CustomUserView(GenericViewSet, ListModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


def home(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Пользователь успешно создан.")
        else:
            return HttpResponse("Не выполнены правила для пароля.")
    else:
        form = CustomUserForm()

    return render(request, 'home.html', {'form': form})
