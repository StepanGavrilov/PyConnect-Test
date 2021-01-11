from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    """
    Аккаунт пользователя
    """
    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    gender_choices = (
        ('f', 'Female'),
        ('m', 'Male')
    )

    username = models.CharField(
        db_index=True,
        unique=True,
        max_length=32,
        blank=False,
        verbose_name='Username'
    )
    email = models.EmailField(
        db_index=True,
        unique=True,
        max_length=32,
        blank=False,
        verbose_name='E-mail'
    )
    first_name = models.CharField(
        max_length=32,
        blank=True,
        verbose_name='First name'
    )
    last_name = models.CharField(
        max_length=32,
        blank=True,
        verbose_name='Last name'
    )
    gender = models.CharField(
        max_length=2,
        choices=gender_choices,
        blank=True,
        verbose_name='Gender'
    )
    age = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name='Age'
    )
    about_me = models.CharField(
        blank=True,
        max_length=1024,
        verbose_name='About me'
    )
    work = models.CharField(
        blank=True,
        max_length=32,
        verbose_name='Work'
    )
    status_work = models.CharField(
        blank=True,
        max_length=32,
        verbose_name='Status work'
    )
    location = models.CharField(
        blank=True,
        max_length=32,
        verbose_name='Location'
    )
    avatar = models.ImageField(
        blank=True,
        verbose_name='Avatar',
        upload_to=f'account/avatar/',
        default='../static/img/account/noimage.png'
    )
    date_joined = models.DateField(
        auto_now_add=True,
        verbose_name='Date joined'
    )
    last_login = models.DateTimeField(
        auto_now=True,
        verbose_name='Last login'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Active'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Staff'
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name='Superuser'
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    EMAIL_FIELD = 'email'

    def __str__(self):
        return f'Id: {self.id}\tUsername: {self.username}'