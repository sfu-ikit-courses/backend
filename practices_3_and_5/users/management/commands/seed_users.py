from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker

User = get_user_model()


class Command(BaseCommand):
    help = "Заполняет базу данных фейковыми пользователями"

    def add_arguments(self, parser):
        parser.add_argument(
            "--total", "-t", type=int, default=5, help="Количество пользователей"
        )
        parser.add_argument(
            "--password",
            "-p",
            type=str,
            default="password123",
            help="Пароль по умолчанию",
        )

    def handle(self, *args, **kwargs):
        total = kwargs["total"]
        password = kwargs["password"]
        fake = Faker("ru_RU")

        users = []

        for _ in range(total):
            username = fake.user_name()
            email = fake.email()

            user = User(
                username=username,
                email=email,
            )
            user.set_password(password)
            users.append(user)

        User.objects.bulk_create(users)

        self.stdout.write(self.style.SUCCESS(f"Успешно создано {total} пользователей."))
        self.stdout.write(self.style.NOTICE(f"Пароль по умолчанию: {password}"))
