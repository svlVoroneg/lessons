from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from .models import Organization, CustomUser
from .serializers import OrganizationSerializer, CustomUserSerializer


class CustomUserView(GenericViewSet, ListModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

"""
        импорты для форм 
( для себя/удобства сделал на стороне сервера интерфейс для авторизации и регистрации новых пользователей)
тестирование параллельной работы "обычного" и REST-API интерфейсов 
"""
from .forms import CustomUserForm
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.views import LoginView, PasswordResetView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView


def index(request):
    return render(request, 'index.html')


class RegisterUserView(CreateView):
    model = CustomUser
    template_name = 'register_user.html'
    form_class = CustomUserForm
    success_url = reverse_lazy('register_done')


class RegisterDoneView(TemplateView):
    template_name = 'register_done.html'


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


class UserLoginView(LoginView):
    template_name = 'login.html'


@login_required
def profile(request):
    return render(request, 'profile.html')


class UserLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'logout.html'
