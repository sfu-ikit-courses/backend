from django.core.management.base import BaseCommand
from django_seed import Seed
from django_seed.seeder import Seeder
from faker import Faker
import random
from library.models import Author, Genre, Library, Book
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()
fake = Faker("ru-RU")


class Command(BaseCommand):
    help = 'Заполнение базы данных сущностями из модуля "Библиотека"'

    def add_arguments(self, parser):
        parser.add_argument("--books", type=int, default=50, help="Количество книг")
        parser.add_argument(
            "--authors", type=int, default=20, help="Количество авторов"
        )
        parser.add_argument("--genres", type=int, default=10, help="Количество жанров")
        parser.add_argument(
            "--libraries", type=int, default=5, help="Количество библиотек"
        )
        parser.add_argument(
            "--employees", type=int, default=10, help="Количество сотрудников"
        )

    def handle(self, *args, **kwargs):
        seeder: Seeder = Seed.seeder(locale="ru_RU")

        seeder.add_entity(
            Author,
            kwargs["authors"],
            {
                "name": lambda x: fake.name(),
                "birth_date": lambda x: fake.date_of_birth(
                    minimum_age=30, maximum_age=80
                ),
            },
        )

        seeder.add_entity(
            Genre,
            kwargs["genres"],
            {
                "name": lambda x: fake.unique.word().capitalize(),
            },
        )

        seeder.execute()

        all_authors = list(Author.objects.all())
        all_genres = list(Genre.objects.all())

        employees = [
            User(
                username=fake.unique.user_name(),
                email=fake.unique.email(),
                password=make_password("password123"),
            )
            for _ in range(kwargs["employees"])
        ]

        created_employees = User.objects.bulk_create(employees)

        libraries = []
        for _ in range(kwargs["libraries"]):
            library = Library(
                name=fake.company() + " Library",
                address=fake.address(),
            )
            libraries.append(library)
        created_libraries = Library.objects.bulk_create(libraries)

        LibraryEmployee = Library.employees.through
        relations = []

        for library in created_libraries:
            assigned_employees = random.sample(
                created_employees, k=random.randint(1, min(3, len(created_employees)))
            )
            for user in assigned_employees:
                relations.append(
                    LibraryEmployee(library_id=library.id, user_id=user.id)
                )

        LibraryEmployee.objects.bulk_create(relations)

        books = []
        books_authors = []
        books_genres = []

        for _ in range(kwargs["books"]):
            book = Book(
                title=fake.sentence(nb_words=4),
                publication_date=fake.date_between(start_date="-20y", end_date="today"),
                isbn=fake.unique.isbn13(separator="-"),
                price=round(random.uniform(10, 100), 2),
                rating=round(random.uniform(0, 10), 1),
                library=random.choice(created_libraries),
            )
            books.append(book)

        created_books = Book.objects.bulk_create(books)

        BookAuthor = Book.authors.through
        BookGenre = Book.genres.through

        for book in created_books:
            authors_sample = random.sample(all_authors, k=random.randint(1, 3))
            genres_sample = random.sample(all_genres, k=random.randint(1, 2))

            books_authors.extend(
                [
                    BookAuthor(book_id=book.id, author_id=author.id)
                    for author in authors_sample
                ]
            )

            books_genres.extend(
                [
                    BookGenre(book_id=book.id, genre_id=genre.id)
                    for genre in genres_sample
                ]
            )

        BookAuthor.objects.bulk_create(books_authors)
        BookGenre.objects.bulk_create(books_genres)

        self.stdout.write(self.style.SUCCESS("База данных успешно заполнена!"))
        self.stdout.write(
            self.style.NOTICE('У всех сотрудников установлен пароль: "password123"')
        )
