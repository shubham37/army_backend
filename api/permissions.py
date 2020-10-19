from rest_framework import permissions

class IsStudentAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated() and (request.user.role == 0)


class IsAssessorAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated() and (request.user.role == 1)


class IsAdminAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated() and (request.user.role == 2)
