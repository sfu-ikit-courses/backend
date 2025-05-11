from django.db import models


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class ArchivedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=False)
