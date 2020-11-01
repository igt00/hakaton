from rest_framework import permissions
from main.models import Teacher, User2, Pupil
from rest_framework.exceptions import PermissionDenied



class TeacherPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if User2.objects.filter(user=request.user).exists():
            if Teacher.objects.filter(user=request.user.user2).exists():
                return True
        raise PermissionDenied


class PupilPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if User2.objects.filter(user=request.user).exists():
            if Pupil.objects.filter(user=request.user.user2).exists():
                return True
        raise PermissionDenied
