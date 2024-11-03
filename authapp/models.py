import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from django.db import models
from rest_framework import serializers

class UserManager(BaseUserManager):

    def create_user(self, username, password=None):
        if username is None:
            raise TypeError('Users must have a username.')

        user = self.model(username=username)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

    def block_users(self, usernames):

        if usernames is None or len(usernames) == 0:
            raise TypeError('No blocked users specified.')

        for username in usernames:
            if username is None:
                raise TypeError('Username is empty.')

            if not (User.objects.filter(username=username) & User.objects.filter(is_staff=False)).exists():
                raise serializers.ValidationError('One or more of the specified users does`t exist or is an administrator.')

        User.objects.filter(username__in=usernames).update(is_active = False)
        return {'usernames': usernames}

    def unlock_users(self, usernames):

        if usernames is None or len(usernames) == 0:
            raise TypeError('No blocked users specified.')

        for username in usernames:
            if username is None:
                raise TypeError('Username is empty.')

            if not User.objects.filter(username=username).exists():
                raise serializers.ValidationError('One or more of the specified users does`t exist.')

        User.objects.filter(username__in=usernames).update(is_active=True)
        return {'usernames': usernames}

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=25, unique=True)

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_username(self):
        return self.username
    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token