from datetime import datetime
from typing import Any

from applications.members.models import WorkPosition, User, TimePreference, Tag


def create_user(username: str,
                first_name: str,
                last_name: str,
                email: str,
                birth_date: datetime,
                position: WorkPosition):
    return User.objects.create(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        birth_date=birth_date,
        position=position,
    )


def update_user(user: User,
                first_name: str | None = None,
                last_name: str | None = None,
                birth_date: datetime | None = None,
                avatar: Any | None = None,
                position: WorkPosition | None = None,
                time_preference: TimePreference | None = None,
                tags: list[int] | None = None) -> User:

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

    if tags is not None:
        user.tags.set(list(Tag.objects.filter(tag__in=tags)))

    user.save()
    return user
