from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, org_id, **extra_fields):
        if not email:
            raise ValueError('email должен быть указан')
        email = self.normalize_email(email)
        user = self.model(email=email, org_id=org_id, **extra_fields)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_user(self, email, password, org_id, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, org_id, **extra_fields)

    def create_superuser(self, email, password, org_id, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        user = self._create_user(email=email, password=password, org_id=org_id, **extra_fields)
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
    email = models.EmailField(unique=True)
    org_id = models.IntegerField(verbose_name='Id организации')
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomAccountManager()

    REQUIRED_FIELDS = ['org_id']
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        '''
        Возвращает first_name и last_name с пробелом между ними.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def natural_key(self):
        return self.email

    def __str__(self):
        return self.email

