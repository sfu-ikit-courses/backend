from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Genre, Author, Library, Book
from .serializers import (
    GenreSerializer,
    AuthorSerializer,
    LibrarySerializer,
    LibraryCreateUpdateSerializer,
    BookSerializer,
    BookCreateUpdateSerializer,
    BookDetailSerializer,
)
from .paginations import StandardResultsSetPagination
from .filters import BookFilter
from drf_spectacular.utils import extend_schema, OpenApiParameter

# Create your views here.


@extend_schema(tags=["Жанр"])
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]
    pagination_class = StandardResultsSetPagination

    @extend_schema(
        summary="Получить все книги в жанре",
        description="Возвращает список книг, относящихся к указанному жанру.",
        responses=BookDetailSerializer(many=True),
    )
    @action(detail=True, methods=["get"], url_path="books")
    def get_books(self):
        genre = self.get_object()
        books = genre.books.all()
        books_page = self.paginate_queryset(books)
        if books_page is not None:
            ser_books = BookDetailSerializer(books_page, many=True)
            return self.get_paginated_response(ser_books.data)

        ser_books = BookDetailSerializer(books, many=True)
        return Response(ser_books.data)

    def get_object(self) -> Genre:
        return super().get_object()


@extend_schema(tags=["Автор"])
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]
    pagination_class = StandardResultsSetPagination

    @extend_schema(
        summary="Получить информацию об авторе (с книгами по запросу)",
        parameters=[
            OpenApiParameter(
                name="include",
                description="Чтобы включить книги: include=books",
                required=False,
                type=str,
            ),
        ],
        responses=AuthorSerializer,
    )
    def retrieve(self, request: Request, *args, **kwargs):
        author = self.get_object()
        serializer = self.get_serializer(author)
        data = serializer.data

        if request.query_params.get("include") == "books":
            books = Book.objects.all()
            data["books"] = BookDetailSerializer(books, many=True).data

        return Response(data)

    @extend_schema(
        summary="Получить 5 самых дорогих книг автора",
        description="Возвращает 5 самых дорогих книг указанного автора, отсортированных по убыванию цены.",
        responses=BookDetailSerializer(many=True),
    )
    @action(detail=True, methods=["get"], url_path="top-books")
    def get_expensive_books(self):
        author = self.get_object()
        top_books = author.books.order_by("-price")[:5]
        sr_top_books = BookDetailSerializer(top_books, many=True)
        return Response(sr_top_books.data)

    def get_object(self) -> Author:
        return super().get_object()

    def get_serializer(self, *args, **kwargs) -> AuthorSerializer:
        return super().get_serializer(*args, **kwargs)


@extend_schema(tags=["Библиотека"])
class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    pagination_class = StandardResultsSetPagination

    @extend_schema(
        summary="Получить книги в библиотеке",
        description="Возвращает список всех книг, хранящихся в указанной библиотеке.",
        responses=BookDetailSerializer(many=True),
    )
    @action(detail=True, methods=["get"], url_path="books")
    def get_books(self):
        genre = self.get_object()
        books = genre.books.all()
        books_page = self.paginate_queryset(books)
        if books_page is not None:
            ser_books = BookDetailSerializer(books_page, many=True)
            return self.get_paginated_response(ser_books.data)

        ser_books = BookDetailSerializer(books, many=True)
        return Response(ser_books.data)

    def get_object(self) -> Library:
        return super().get_object()

    def get_permissions(self):
        if self.action in ["create", "destroy", "update", "partial_update"]:
            return [IsAdminUser()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return LibraryCreateUpdateSerializer
        return LibrarySerializer


@extend_schema(tags=["Книга"])
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related("library").prefetch_related(
        "authors", "genres"
    )
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    search_fields = ["title", "author__name"]
    ordering_fields = ["title", "publication_date", "isbn"]
    ordering = ["title"]
    pagination_class = StandardResultsSetPagination

    def destroy(self, request: Request, *args, **kwargs):
        book = self.get_object()
        user = request.user

        if not book.library.employees.filter(id=user.id).exists():
            raise PermissionDenied("Вы не можете удалять книги из этой библиотеки.")

        return super().destroy(request, *args, **kwargs)

    def get_object(self) -> Book:
        return super().get_object()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return BookCreateUpdateSerializer
        if self.action == "list":
            return BookDetailSerializer
        return BookSerializer

    @extend_schema(
        summary="Топ 10 книг по рейтингу",
        description="Возвращает 10 книг с наивысшим значением рейтинга (по убыванию поля `rating`).",
        responses=BookDetailSerializer(many=True),
    )
    @action(detail=False, methods=["get"], url_path="top")
    def get_top_books(self):
        top_books = Book.objects.order_by("-rating")[:10]
        sr_top_books = BookDetailSerializer(top_books, many=True)
        return Response(sr_top_books.data)
