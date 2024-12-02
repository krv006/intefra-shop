from django.contrib.auth.models import AbstractUser
from django.db.models import BooleanField, EmailField, CharField, TextChoices, OneToOneField, DateField, SET_NULL, Model

from shops.models import TimeBaseModel
from users.managers import CustomUserManager


class User(AbstractUser):
    class Type(TextChoices):
        OPERATOR = 'operator', 'Operator'
        ADMIN = 'admin_side', 'Admin_side'
        USER = 'user', 'User'

    username = None
    first_name = None
    last_name = None
    email = EmailField(unique=True)
    name = CharField(max_length=255)
    is_active = BooleanField(default=False)
    type = CharField(max_length=25, choices=Type.choices, default=Type.USER, verbose_name="user type")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


class Operator(Model):
    user = OneToOneField('users.User', SET_NULL, null=True, blank=True, related_name='operators',
                         verbose_name='User', limit_choices_to={'type': 'Operator'})
    passport = CharField(max_length=30, unique=True, verbose_name="passport id for operator")
    start_date = DateField(null=True, blank=True, verbose_name='time to start work')
    end_date = DateField(null=True, blank=True, verbose_name='time to end work')

    class Meta:
        verbose_name = 'Operator'
        verbose_name_plural = 'Operators'
