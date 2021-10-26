from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Organization, CustomUser


class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = ('name', )


class CustomUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'organization', 'first_name', 'last_name')
        error_css_class = 'error'
