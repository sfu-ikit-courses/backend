from django.http import HttpResponseForbidden
from functools import wraps
from .models import Article


def author_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        article_id = kwargs.get("article_id") or kwargs.get("id") or kwargs.get("pk")
        if not article_id:
            return HttpResponseForbidden("Не указан ID статьи.")

        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            return HttpResponseForbidden("Статья не найдена.")

        if article.author != request.user:
            return HttpResponseForbidden("Вы не автор этой статьи.")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
