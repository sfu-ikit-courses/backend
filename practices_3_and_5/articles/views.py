from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http.response import HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .decorators import author_required
from .models import Article, Tag, Category
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from .forms import ArticleForm
from django.core.paginator import Paginator
from .filters import ArticleFilter


def articles(request):

    article_filter = ArticleFilter(
        request.GET,
        queryset=Article.active_objects.all()
        .select_related("category")
        .prefetch_related("tags"),
    )
    articles = article_filter.qs

    paginator = Paginator(articles, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(
        request,
        "articles/index.html",
        {
            "articles": page_obj,
            "categories": categories,
        },
    )


@login_required
def article_create(request):
    if request.method == "POST":
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, "Статья успешно создана!")
            return redirect("article.index")
    else:
        article_form = ArticleForm()
    return render(request, "articles/create.html", {"article_form": article_form})


@login_required
@author_required
def article_update(request, article_id):
    # article = Article.objects.get(id=article_id)
    article = get_object_or_404(Article, pk=article_id)

    if request.method == "POST":
        article_form = ArticleForm(request.POST, request.FILES, instance=article)
        if article_form.is_valid():
            article_form.save()
            next_url = (
                request.GET.get("next")
                or request.META.get("HTTP_REFERER")
                or reverse("article.index")
            )
            return HttpResponseRedirect(next_url)
    else:
        article_form = ArticleForm(instance=article)
    return render(
        request,
        "articles/update.html",
        {"article_form": article_form, "article": article},
    )


@login_required
@author_required
def article_delete(request, article_id):

    if request.method == "POST":
        article = Article.objects.get(pk=article_id)
        article.delete(soft=True)
        return HttpResponseRedirect(reverse("article.index"))
    else:
        pass


def articles_by_tag(request: HttpRequest, tag_slug: str) -> HttpResponse:
    tag = get_object_or_404(Tag, slug=tag_slug)
    articles = Article.objects.filter(tags=tag)

    return render(request, "articles/tag-list.html", {"articles": articles, "tag": tag})


def articles_by_category(request: HttpRequest, category_slug: str) -> HttpResponse:
    category = get_object_or_404(Category, slug=category_slug)
    articles = Article.objects.filter(category=category)

    return render(
        request,
        "articles/category-list.html",
        {"articles": articles, "category": category},
    )


def articles_by_slug(request: HttpRequest, slug: str) -> HttpResponse:
    article = get_object_or_404(Article, slug=slug)

    return render(request, "articles/detail-view.html", {"article": article})


@login_required
def archive(request: HttpRequest) -> HttpResponse:
    archive_articles = Article.archived_objects.filter(author=request.user)

    return render(request, "articles/archive.html", {"articles": archive_articles})


@require_POST
@login_required
@author_required
def article_restore(request: HttpRequest, id: int) -> HttpResponse:
    article = get_object_or_404(Article.archived_objects, pk=id)

    article.active = True
    article.save()

    return redirect("article.archive")


@require_POST
@login_required
@author_required
def article_force_delete(request: HttpRequest, id: int) -> HttpResponse:
    article = get_object_or_404(Article.archived_objects, pk=id)

    article.delete()

    return redirect("article.archive")
