from django.core.management.base import BaseCommand
from articles.models import Category, Tag
from faker import Faker


class Command(BaseCommand):
    help = "Заполняет базу данных тестовыми категориями и тегами"

    def add_arguments(self, parser):
        parser.add_argument(
            "--categories",
            "-c",
            type=int,
            default=5,
            help="Количество категорий для создания",
        )
        parser.add_argument(
            "--tags",
            "-t",
            type=int,
            default=5,
            help="Количество тегов для создания",
        )

    def handle(self, *args, **kwargs):
        total_categories = kwargs["categories"]
        total_tags = kwargs["tags"]

        fake = Faker("ru-RU")

        categories = []

        for _ in range(total_categories):
            category = Category(name=fake.word())
            categories.append(category)

        tags = []

        for _ in range(total_tags):
            tag = Tag(name=fake.word())
            tags.append(tag)

        Category.objects.bulk_create(categories)
        Tag.objects.bulk_create(tags)

        self.stdout.write(
            self.style.SUCCESS(
                f"Успешно создано {total_categories} категорий и {total_tags} тегов"
            )
        )
