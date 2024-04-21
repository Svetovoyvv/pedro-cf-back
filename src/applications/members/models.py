import pathlib

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from applications.common.file_uploads import upload_to


class Tag(models.Model):
    name = models.CharField(max_length=255)


class WorkPosition(models.Model):
    name = models.CharField(max_length=255)


def upload_avatar(instance: 'User', filename: str) -> pathlib.Path:
    return upload_to('avatar', instance, filename)


class User(AbstractUser):
    birth_date = models.DateField(
        null=True,
        blank=True,
    )
    position = models.ForeignKey(
        WorkPosition,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    tags = models.ManyToManyField(
        Tag,
    )
    about = models.TextField(
        null=True,
        blank=True,
    )
    time_preference = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    avatar = models.ImageField(
        upload_to=upload_avatar,
        null=True,
        blank=True,
    )

    @property
    def ages(self):
        if self.birth_date is not None:
            return relativedelta(timezone.now().date() - self.birth_date).years
        return None

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'User {self.pk} | {self.get_full_name()} | {self.username}'
