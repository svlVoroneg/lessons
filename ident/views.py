from rest_framework.viewsets import ModelViewSet
from .models import CustomUser
from .forms import CustomUserForm
from .serializers import CustomUserSerializer
from django.shortcuts import render
from django.http import HttpResponse


class IdentViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


def home(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Пользователь успешно создан.")
        else:
            return HttpResponse("Ошибка создания.")
    else:
        form = CustomUserForm()

    return render(request, 'home.html', {'form': form})
