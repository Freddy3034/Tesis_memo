from rest_framework import permissions
class IsDirector(permissions.BasePermission):
    """
    Permite acceso solo si el usuario tiene rol de Director'
    """ 
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol =='Director'

class IsFuncionario(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated