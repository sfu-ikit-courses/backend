from django.db import models
from slugify import slugify
from django.utils.html import strip_tags
from django.utils.text import Truncator


class SluggedModel(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Имя")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Слаг")

    class Meta:
        abstract = True
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(SluggedModel):
    class Meta(SluggedModel.Meta):
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Tag(SluggedModel):
    class Meta(SluggedModel.Meta):
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Article(SluggedModel):
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
            self.excerpt = Truncator(strip_tags(self.content)).chars(100)
        super().save(*args, **kwargs)
