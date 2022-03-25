from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(verbose_name='Персонал', default=False)
    admin = models.BooleanField(verbose_name='Администратор', default=False)

    name = models.CharField(max_length=100, verbose_name='Имя', blank=True)
    surname = models.CharField(max_length=100, verbose_name='Фамилия', blank=True)
    phone_number = models.CharField(max_length=15, verbose_name='Контактный номер телефона', blank=True)
    street = models.CharField(max_length=50, verbose_name='Улица', blank=True)
    house = models.CharField(max_length=50, verbose_name='Дом', blank=True)
    flat = models.CharField(max_length=50, verbose_name='Квартира', blank=True, null=True)

    # поле password уже определено

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email и Password предложены изначально

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def short_name(self):
        """Возвращает имя"""
        return self.name

    def full_name(self):
        """Возвращает имя и фамилию"""
        return self.name + ' ' + self.surname

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Является ли пользователь персоналом?"""
        return self.staff

    @property
    def is_admin(self):
        """Является ли пользователь админом?"""
        return self.admin
