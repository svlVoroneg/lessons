from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from .models import CustomUser, Organization


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('organization', 'email', 'first_name', 'last_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'organization', 'is_staff', 'is_activated')
    list_filter = ('is_activated',)
    fieldsets = (
        (None, {'fields': ('organization', 'email', 'password')}),
        (_('Personal info'), {'fields': (('first_name', 'last_name'),)}),
        (_('Permissions'), {'fields': (('is_active', 'is_staff'), 'groups', 'user_permissions'), }),
        (_('Important dates'), {
            'classes': ('collapse',),
            'fields': (('last_login', 'date_joined'),)
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('organization', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)


admin.site.register(Organization)
admin.site.register(CustomUser, UserAdmin)
