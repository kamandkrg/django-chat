from django.contrib.auth.models import PermissionsMixin
from djongo import models
from django.contrib.auth.base_user import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField

from account.manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    MALE = "M"
    FEMALE = "F"
    UNSURE = "U"
    SEX_CHOICE = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (UNSURE, 'Unsure')
    )
    first_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(max_length=15, unique=True)
    username = models.CharField(unique=True, max_length=32)
    image = models.ImageField(null=True, upload_to='account/')
    bio = models.TextField(null=True, blank=True)
    online = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICE, default=UNSURE)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return str(self.pk)

    def change_connection(self):
        self.online = not self.online
        return self.online












