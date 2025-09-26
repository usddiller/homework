from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from users.views import ActivateAccountByEmail
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import (
    RegistrationViewSet,
    ActivateAccount,
    UserModelViewSet,
    FriendInvitesView,
)
from images.views import ImageViewSet


router = DefaultRouter()
router.register(
    prefix="registration",
    viewset=RegistrationViewSet,
    basename="registration",
)
router.register(
    prefix="users", viewset=UserModelViewSet, basename="users"
)
router.register(
    prefix="invites", viewset=FriendInvitesView, basename="invites"
)
router.register(prefix="images", viewset=ImageViewSet, basename="images")

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="News Service API",
        default_version="v1",
        description="Сервис новостей с авторизацией (JWT). Эндпоинты: регистрация/активация, токены, статьи.",
        contact=openapi.Contact(email="admin@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

template_patterns = [
    path(
        route="",
        view=TemplateView.as_view(template_name="api/base.html"),
        name="base",
    ),
]
from posts.views import ArticleViewSet  # добавить к импортам

router.register(prefix="articles", viewset=ArticleViewSet, basename="articles")

urlpatterns = (
    [
          path("auth/activate/", ActivateAccountByEmail.as_view(), name="auth-activate-by-email"),
        # твой GET-активатор:
        path("activate/<int:pk>/", ActivateAccount.as_view(), name="activate-account"),
        path(route="", view=include(template_patterns)),
        path(route="admin/", view=admin.site.urls),
        path(
            route="api/token/",
            view=TokenObtainPairView.as_view(),
            name="token_obtain_pair",
        ),
        path(
            route="api/token/refresh/",
            view=TokenRefreshView.as_view(),
            name="token_refresh",
        ),
        path(route="api/v1/", view=include(router.urls)),
        path(
            route="swagger/",
            view=schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "activate/<int:pk>/",
            ActivateAccount.as_view(),
            name="activate-account",
        ),
    ]
    + debug_toolbar_urls()
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
