from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework import mixins, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema

from users.serializers import (
    UserModelSerializer, FriendInviteSerializer,
    CreateFriendInviteSerializer
)
from users.models import Client, FriendInvite
from common.paginators import CustomPageNumberPagination
from common.permissions import IsOwnerOrAdmin
from common.filters import SearchFilter


class RegistrationViewSet(mixins.CreateModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    queryset = Client.objects.all()
    serializer_class = UserModelSerializer
    parser_classes = [MultiPartParser, FormParser]


class ActivateAccount(APIView):
    permission_classes = [AllowAny]

    def _wants_json(self, request) -> bool:
        accept = request.META.get("HTTP_ACCEPT", "")
        return "application/json" in accept.lower()

    def get(self, request: Request, pk: int) -> Response:
        code = request.query_params.get("code")
        try:
            user: Client = Client.objects.get(pk=pk, activation_code=code)
        except Client.DoesNotExist:
            if self._wants_json(request):
                raise NotFound(detail="activation link invalid")
            return render(request, "api/activation_failed.html")
        now = timezone.now()
        if now > user.expired_code:
            if self._wants_json(request):
                raise PermissionDenied(detail="code expired")
            return render(request, "api/activation_failed.html")
        user.is_active = True
        user.save(update_fields=["is_active"])
        if self._wants_json(request):
            return Response({"message": "activation success!"})
        return render(request, "api/activation_success.html")
    

class UserModelViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    permission_classes = [IsOwnerOrAdmin]
    queryset = Client.objects.all().select_related("avatar")
    serializer_class = UserModelSerializer
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ["username", "email"]
    sort_by_fields = []

    @method_decorator(cache_page(timeout=600))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(timeout=600))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class FriendInvitesView(ViewSet):
    permission_classes = [IsOwnerOrAdmin]
    pagination_class = CustomPageNumberPagination

    @swagger_auto_schema(
        responses={
            200: FriendInviteSerializer
        }
    )
    def list(self, request: Request):
        invites = FriendInvite.objects.filter(
            from_client=request.user
        )
        serializer = FriendInviteSerializer(
            instance=invites, many=True, 
        )
        return Response(data=serializer.data)

    @swagger_auto_schema(
        request_body=CreateFriendInviteSerializer,
        responses={
            201: "invite created",
            400: "validation error",
            403: "permission error"
        }
    )
    def create(self, request: Request):
        serializer = CreateFriendInviteSerializer(
            data=request.data, context={
                "user": request.user,
            }
        )
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except Exception as e:
            raise ValidationError(detail=str(e))
        return Response(
            data={"message": "invite created"},
            status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(
        request_body=CreateFriendInviteSerializer,
        responses={
            200: "success",
            400: "validation error",
            403: "not authorized",
            404: "not found"
        }
    )
    def partial_update(self, request: Request, pk: int):
        invite: FriendInvite = get_object_or_404(
            FriendInvite, pk=pk
        )
        serializer = CreateFriendInviteSerializer(
            instance=invite, data=request.data, partial=True,
            context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={"message": "success"})

    @swagger_auto_schema(
        responses={
            200: "success",
            403: "forbidden",
            404: "not found"
        }
    )
    def destroy(self, request: Request, pk: int):
        invite: FriendInvite = get_object_or_404(
            FriendInvite, pk=pk
        )
        invite.delete()
        return Response(data={"message": "success"})

# QUERY_PARAMS
# search - поиск по значению
# orderBy (asc/desc) - сортировка по убыванию/возрастанию
# filter/sortBy - сортировка по каким нибудь атрибутам 
# http://localhost/api/users/&search=Иван Иванов&sortBy=birthday&orderBy=asc