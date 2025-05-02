from django.contrib.sitemaps import Sitemap
from .models import Article
from django.urls import reverse


class ArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Article.active_objects.all()

    def lastmod(self, obj: Article):
        return obj.updated_at

    def location(self, obj: Article):
        return reverse("article.detail", args=(obj.slug,))
