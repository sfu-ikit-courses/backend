from django.db import models
from django.urls import reverse


class Post(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    description = models.TextField(verbose_name="Описание")
    featured_image = models.ImageField(
        blank=True, default="default.jpg", upload_to="images/"
    )

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.name}"
