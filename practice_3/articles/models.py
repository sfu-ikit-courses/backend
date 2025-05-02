from django.db import models
from slugify import slugify
from django.utils.html import strip_tags
from django.utils.text import Truncator
from .managers import ActiveManager, ArchivedManager
from datetime import datetime


class SluggedModel(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Слаг")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.slug and self.name:
            self.generate_slug()

    class Meta:
        abstract = True
        ordering = ["name"]

    def __str__(self):
        return self.name

    def generate_slug(self):
        if not self.slug:
            self.slug = (
                slugify(self.name) + "-" + str(round(datetime.now().timestamp()))
            )
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.generate_slug()
        super().save(*args, **kwargs)


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ActiveModel(models.Model):
    active = models.BooleanField(default=True)

    active_objects = ActiveManager()
    archived_objects = ArchivedManager()
    objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, soft=False):
        if soft:
            self.active = False
            self.save()
        else:
            super().delete()


class Category(SluggedModel):
    class Meta(SluggedModel.Meta):
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        unique_together = ("name",)


class Tag(SluggedModel):
    class Meta(SluggedModel.Meta):
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        unique_together = ("name",)


class Article(SluggedModel, TimeStampedModel, ActiveModel):
    content = models.TextField(verbose_name="Описание")
    excerpt = models.CharField(max_length=100, verbose_name="Отрывок")
    featured_image = models.ImageField(
        blank=True, default="default.jpg", upload_to="images/"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="articles"
    )
    tags = models.ManyToManyField(Tag, related_name="articles")

    class Meta(SluggedModel.Meta):
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def save(self, *args, **kwargs):
        if not self.excerpt and self.content:
            self.excerpt = strip_tags(self.content)

        if len(self.excerpt) > 80:
            self.excerpt = self.excerpt[:80] + "..."

        super().save(*args, **kwargs)
