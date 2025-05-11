from django.core.management.base import BaseCommand
from articles.models import Article, Category, Tag
from faker import Faker
from base.utils import get_plural_form
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Заполняет базу данных фейковыми статьями"

    def add_arguments(self, parser):
        parser.add_argument(
            "--total", "-t", type=int, default=5, help="Количество статей для создания"
        )

    def handle(self, *args, **kwargs):

        total = kwargs["total"]
        fake = Faker("ru-RU")

        categories = Category.objects.all()
        tags = Tag.objects.all()

        if not Category.objects.exists() or not Tag.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    "Перед созданием статей необходимо добавить категории и теги!"
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    "Используйте команды: python manage.py seed_categories_and_tags"
                )
            )
            return

        users = User.objects.all()

        if not users.exists():
            self.stdout.write(
                self.style.WARNING("Создайте хотя бы одного пользователя.")
            )
            return

        articles = []

        for _ in range(total):
            article = Article(
                name=fake.sentence(),
                content=fake.text(),
                excerpt=fake.sentence(),
                category=fake.random_element(categories),
                author=fake.random_element(users),
            )

            articles.append(article)

        created_articles = Article.objects.bulk_create(articles)

        ArticleTag = Article.tags.through
        bulk_relations = []

        for article in created_articles:
            random_tags = fake.random_elements(
                elements=list(tags), length=3, unique=True
            )
            for tag in random_tags:
                bulk_relations.append(ArticleTag(article_id=article.id, tag_id=tag.id))

        ArticleTag.objects.bulk_create(bulk_relations)

        verb = get_plural_form(total, one="создана", few="созданы", many="создано")
        noun = get_plural_form(total, one="статья", few="статьи", many="статей")

        self.stdout.write(self.style.SUCCESS(f"Успешно {verb} {total} {noun}"))
