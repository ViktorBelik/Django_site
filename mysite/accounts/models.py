import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
import shutil
import os

"""Вместо прямого обращения к User следует обращаться к пользовательской модели
с помощью django.contrib.auth.get_user_model(). Этот метод вернёт текущую
активную пользовательскую модель — пользовательскую модель, если она указана,
или User в противном случае.
При определении внешнего ключа или связей «многие ко многим»
с моделью пользователя необходимо указать пользовательскую модель
с помощью параметра AUTH_USER_MODEL.
"""


def user_avatar_directory_path(instance: "User", filename: str) -> str:
    path = "users/user_{username}/avatar".format(
        username=instance.username,
    )
    path_to_dir = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(path_to_dir):
        shutil.rmtree(path_to_dir)
    path_to_file = os.path.join(path, filename)
    return path_to_file


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    email = models.EmailField(
        verbose_name=_("Email address"),
        null=False,
        blank=False,
        unique=True,
    )
    phone = PhoneNumberField(
        verbose_name=_("Phone number"),
        null=True,
        blank=True,
        unique=True,
    )
    date_birth = models.DateField(
        verbose_name=_("Date of birth"),
        null=True,
        blank=True,
    )
    about_me = models.TextField(
        max_length=500,
        blank=True,
    )
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to=user_avatar_directory_path,
    )
    agreement_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username} (id: {self.id})'
