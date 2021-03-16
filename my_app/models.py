from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password=None, **extra_fields):
        """
        Создает и возвращает `User` с именем пользователя и паролем.
        """

        if not username:
            raise ValueError('Указанное имя пользователя должно быть установлено')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def update_user(self, instance, password=None, **extra_fields):
        """
        Обновляет и возвращает `User` с именем пользователя и паролем.
        """
        for attr, value in extra_fields.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save(using=self._db)

        return instance


class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token
