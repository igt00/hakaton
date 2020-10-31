from rest_framework import permissions
from main.models import Teacher, User2, Pupil
from rest_framework.exceptions import PermissionDenied



class TeacherPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if User2.objects.filter(user=request.user).exists():
            if Teacher.objects.filter(user=request.user.user2).exists():
                return True
        raise PermissionDenied


class IsOwnerOrReadOnlyPypil(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if User2.objects.filter(user=request.user).exists():
            if Pupil.objects.filter(user=request.user.user2).exists():
                return True
        raise PermissionDenied
