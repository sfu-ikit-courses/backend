"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from base.views import page_not_found
from django.contrib.sitemaps.views import sitemap
from articles.sitemaps import ArticleSitemap
from debug_toolbar.toolbar import debug_toolbar_urls

sitemaps = {
    "articles": ArticleSitemap,
}

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("ckeditor5/", include("django_ckeditor_5.urls")),
        path("articles/", include("articles.urls")),
        path("posts/", include("blogs.urls")),
        path(
            "sitemap.xml/",
            sitemap,
            {"sitemaps": sitemaps},
            name="django.contrib.sitemaps.views.sitemap",
        ),
        path("auth/", include("users.urls")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + debug_toolbar_urls()
)


handler404 = page_not_found
