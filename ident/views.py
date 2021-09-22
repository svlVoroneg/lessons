from rest_framework.viewsets import ModelViewSet
from .models import Organization, CustomUser
from .forms import CustomUserForm
from .serializers import OrganizationSerializer, CustomUserSerializer
from django.shortcuts import render
from django.http import HttpResponse


class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


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
