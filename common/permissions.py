from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from users.models import Client


class IsOwnerOrAdmin(BasePermission):
    """
    Пускаем только владельца объекта или администратора.
    ❗ Работает только с ModelViewSet, где obj — это User или модель с полем `user`.

    Аргументы метода has_permission:
        request (rest_framework.request.Request): HTTP-запрос
        view (rest_framework.viewsets.ModelViewSet): вьюха (можно использовать .action)

    Аргументы метода has_object_permission:
        obj (models.Model): объект, к которому проверяется доступ (обычно результат .get_object())

    Возвращает:
        bool: True — доступ разрешён, False — доступ запрещён
    """

    def has_permission(self, request: Request, view: ModelViewSet) -> bool:
        # Разрешаем только авторизованным (в том числе админам)
        return request.user.is_authenticated

    def has_object_permission(
        self, request: Request, view: ModelViewSet, obj: Client | None
    ):
        if view.action in ["list", "retrieve"]:
            return True
        return obj == request.user or request.user.is_staff  
