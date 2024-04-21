from datetime import datetime
from typing import Any

from django.db import IntegrityError

from applications.common.exceptions import BaseServiceException
from applications.members.models import WorkPosition, User, Tag


def create_user(username: str,
                first_name: str,
                last_name: str,
                email: str,
                birth_date: datetime,
                position: WorkPosition):
    try:
        return User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            birth_date=birth_date,
            position=position,
        )
    except IntegrityError as e:
        raise BaseServiceException(
            'Ошибка создания пользователя'
        ) from e


def update_user(user: User,
                first_name: str | None = None,
                last_name: str | None = None,
                birth_date: datetime | None = None,
                about: str | None = None,
                avatar: Any | None = None,
                position: WorkPosition | None = None,
                time_preference: str | None = None,
                tags: str | None = None) -> User:

    if first_name is not None:
        user.first_name = first_name

    if last_name is not None:
        user.last_name = last_name

    if birth_date is not None:
        user.birth_date = birth_date

    if avatar is not None:
        user.avatar = avatar

    if position is not None:
        user.position = position

    if time_preference is not None:
        user.time_preference = time_preference

    if about is not None:
        user.about = about

    if tags is not None:
        tags = [int(tag) for tag in tags.split(',')]
        user.tags.set(list(Tag.objects.filter(id__in=tags)))

    user.save()
    return user


def create_tag(name: str):
    tag, _ = Tag.objects.get_or_create(name=name)
    return tag
