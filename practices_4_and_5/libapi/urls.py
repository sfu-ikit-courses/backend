from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from library.routers import router as library_router
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

main_router = DefaultRouter()
main_router.registry.extend(library_router.registry)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/<str:version>/", include(main_router.urls)),
    path("api/<str:version>/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/<str:version>/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/<str:version>/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path(
        "api/<str:version>/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/<str:version>/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "api/<str:version>/token/verify/",
        TokenVerifyView.as_view(),
        name="token_verify",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
