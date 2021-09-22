from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager


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

    def create_user(self, email, password, оrganization, **extra_fields):
        if not email:
            raise ValueError('email должен быть указан')
        try:
            cur_org = Organization.objects.get(pk=оrganization)
        except Organization.DoesNotExist:
            raise ValueError('Указана несуществующая организация')
        email = self.normalize_email(email)
        user = self.model(email=email, оrganization=cur_org, **extra_fields)
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
        user = self.model(email=email, оrganization=cur_org, **extra_fields)
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
    оrganization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Организация')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, blank=True, verbose_name='Фамилия')
    is_staff = models.BooleanField(default=False, verbose_name='Сотрудник')

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'

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
