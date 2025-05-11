from rest_framework import serializers
from .models import Author, Genre, Library, Book
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "birth_date"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class LibrarySerializer(serializers.ModelSerializer):
    employees = UserSerializer(many=True)

    class Meta:
        model = Library
        fields = ["id", "name", "address", "employees"]


class LibraryCreateUpdateSerializer(serializers.ModelSerializer):
    employees = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all()
    )

    class Meta:
        model = Library
        fields = ["id", "name", "address", "employees"]


class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "rating", "image"]


class BookSerializer(serializers.ModelSerializer):
    library = LibrarySerializer()
    authors = AuthorSerializer(many=True)
    genres = GenreSerializer(many=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "publication_date",
            "isbn",
            "price",
            "rating",
            "image",
            "library",
            "authors",
            "genres",
        ]


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Author.objects.all()
    )

    genres = GenreSerializer(
        many=True, required=False, style={"base_template": "textarea.html"}
    )
    genre_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        style={"base_template": "textarea.html"},
    )

    class Meta:
        model = Book
        fields = [
            "title",
            "publication_date",
            "isbn",
            "price",
            "rating",
            "image",
            "library",
            "authors",
            "genres",
            "genre_ids",
        ]

    def validate(self, data):
        if "genres" in data and "genre_ids" in data:
            raise serializers.ValidationError(
                "Укажите либо 'genres', либо 'genre_ids', но не оба."
            )
        if "genres" not in data and "genre_ids" not in data:
            raise serializers.ValidationError(
                "Необходимо указать либо 'genres', либо 'genre_ids'."
            )
        return data

    def create(self, validated_data):
        genres_data = validated_data.pop("genres", None)
        genre_ids = validated_data.pop("genre_ids", None)
        authors = validated_data.pop("authors", [])

        genres = []
        if genre_ids:
            genres = list(Genre.objects.filter(id__in=genre_ids))
            if len(genres) != len(genre_ids):
                raise serializers.ValidationError(
                    "Один или несколько genre_ids не найдены."
                )
        elif genres_data:
            for genre_data in genres_data:
                genre, _ = Genre.objects.get_or_create(name=genre_data["name"])
                genres.append(genre)

        book = Book.objects.create(**validated_data)
        book.genres.set(genres)
        book.authors.set(authors)

        return book

    def update(self, instance: Book, validated_data):
        genres_data = validated_data.pop("genres", None)
        genre_ids = validated_data.pop("genre_ids", None)
        authors = validated_data.pop("authors", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if genre_ids is not None:
            genres = list(Genre.objects.filter(id__in=genre_ids))
            if len(genres) != len(genre_ids):
                raise serializers.ValidationError(
                    "Один или несколько genre_ids не найдены."
                )
            instance.genres.set(genres)
        elif genres_data is not None:
            genres = []
            for genre_data in genres_data:
                genre, _ = Genre.objects.get_or_create(name=genre_data["name"])
                genres.append(genre)
            instance.genres.set(genres)

        if authors is not None:
            instance.authors.set(authors)

        return instance
