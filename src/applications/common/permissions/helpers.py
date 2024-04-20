from rest_framework.permissions import BasePermission

from applications.common.permissions.default_groups import GroupNames
from applications.members.models import User


def is_user_has_group(user: User, group: GroupNames) -> bool:
    return user.groups.filter(name=group.value).exists()


def is_admin(user: User) -> bool:
    return is_user_has_group(user, GroupNames.ADMIN)


class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        return is_admin(request.user)
