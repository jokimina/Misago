from rest_framework.permissions import SAFE_METHODS, BasePermission

from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext as _
from misago.conf import settings


class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous and (request.method not in SAFE_METHODS)\
                and (request.path not in settings.ANON_REST_LIST):
            raise PermissionDenied(_("This action is not available to guests."))
        else:
            return True
