from django.contrib.auth.backends import BaseBackend
from django.core.validators import validate_email
from django.db.models import Q
from django.shortcuts import get_object_or_404

from account.models import User
import phonenumbers


class MyBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None):
        number = phonenumbers.parse(username, None)
        if phonenumbers.is_valid_number(number):
            user = get_object_or_404(User, phone=username)
        elif "@" in username:
            user = get_object_or_404(User, email=username)
        else:
            user = get_object_or_404(User, username=username)
        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
