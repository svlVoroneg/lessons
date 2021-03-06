from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Organization(models.Model):
    name = models.CharField(
        max_length=64, verbose_name='Наименование организации',
        unique=True, default='Владелец системы')

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.name


class CustomAccountManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, organization, **extra_fields):
        if not email:
            raise ValueError('email должен быть указан')
        try:
            cur_org = Organization.objects.get(pk=organization)
        except Organization.DoesNotExist:
            raise ValueError('Указана несуществующая организация')
        email = self.normalize_email(email)
        user = self.model(email=email, organization=cur_org, **extra_fields)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError('email должен быть указан')
        try:
            cur_org = Organization.objects.get(pk=1)
        except Organization.DoesNotExist:
            cur_org = Organization(name='Владелец системы')
            cur_org.save()
        email = self.normalize_email(email)
        user = self.model(email=email, organization=cur_org, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email_):
        print(email_)
        return self.get(email=email_)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Подкласс Django AbstractBaseUser, содержит обязательные поля:
    1 - password
    2 - last_login
    3 - is_active
    """
    email = models.EmailField(unique=True, verbose_name='Е-mail(логин)')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Организация')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, blank=True, verbose_name='Фамилия')
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_activated = models.BooleanField(default=True, verbose_name='Прошел активацию?')

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['organization']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def natural_key(self):
        return self.email

    def __str__(self):
        return self.email
