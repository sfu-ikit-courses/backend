from django.urls import path
from . import views

urlpatterns = [
    path("", views.articles, name="article.index"),  # R
    path("create/", views.article_create, name="article.create"),  # C
    path("update/<int:article_id>/", views.article_update, name="article.update"),  # U
    path("remove/<int:article_id>/", views.article_delete, name="article.delete"),  # D
    path("tags/<slug:tag_slug>/", views.articles_by_tag, name="article.by_tag"),
    path(
        "category/<slug:category_slug>/",
        views.articles_by_category,
        name="article.by_category",
    ),
    path("archive/", views.archive, name="article.archive"),
    path("restore/<int:id>/", views.article_restore, name="article.restore"),
    path(
        "force-delete/<int:id>/",
        views.article_force_delete,
        name="article.force_delete",
    ),
    path(
        "<slug:slug>/",
        views.articles_by_slug,
        name="article.detail",
    ),
]
