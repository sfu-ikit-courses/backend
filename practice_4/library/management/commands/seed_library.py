from django.core.management.base import BaseCommand
from django_seed import Seed
from django_seed.seeder import Seeder
from faker import Faker
import random
from library.models import Author, Genre, Library, Book

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

        seeder.add_entity(
            Library,
            kwargs["libraries"],
            {
                "name": lambda x: fake.company() + " Library",
                "address": lambda x: fake.address(),
            },
        )

        seeder.execute()

        all_authors = list(Author.objects.all())
        all_genres = list(Genre.objects.all())
        all_libraries = list(Library.objects.all())

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
                library=random.choice(all_libraries),
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
