from django import forms
from django.forms import ModelForm
from .models import Article
from django_ckeditor_5.widgets import CKEditor5Widget


class ArticleForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["excerpt"].required = False

    class Meta:
        model = Article
        fields = ["name", "content", "excerpt", "tags", "category", "featured_image"]

        widgets = {
            "content": CKEditor5Widget(config_name="default"),
        }

        labels = {"excerpt": Article._meta.get_field("excerpt").verbose_name}
