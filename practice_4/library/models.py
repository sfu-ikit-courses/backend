from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from typing import TYPE_CHECKING

# Create your models here.

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager


class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    birth_date = models.DateField(verbose_name="Дата рождения")
    books: "RelatedManager[Book]"

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    books: "RelatedManager[Book]"

    def __str__(self):
        return self.name


class Library(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    address = models.TextField(blank=True, null=True, verbose_name="Адрес")
    books: "RelatedManager[Book]"

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    publication_date = models.DateField(verbose_name="Дата публикации")
    isbn = models.CharField(unique=True, verbose_name="ISBN")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Цена")
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        verbose_name="Рейтинг",
    )
    image = models.ImageField(
        upload_to="books/",
        blank=True,
        default="default.png",
        verbose_name="Изображение",
    )
    library = models.ForeignKey(
        Library,
        on_delete=models.CASCADE,
        related_name="books",
        verbose_name="Библиотека",
    )
    authors = models.ManyToManyField(
        Author, related_name="books", verbose_name="Авторы"
    )
    genres = models.ManyToManyField(Genre, related_name="books", verbose_name="Жанры")

    def __str__(self):
        return self.title
