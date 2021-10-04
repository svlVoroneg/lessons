from django.conf.urls import url, include
from django.urls import path
from .views import home, UserLoginView, profile, UserLogoutView, index, RegisterUserView, RegisterDoneView

urlpatterns = [
    path('accounts/login', UserLoginView.as_view(), name='login'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/logout/', UserLogoutView.as_view(), name='logout'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('', index, name='index'),
]
