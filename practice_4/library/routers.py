from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, GenreViewSet, LibraryViewSet, BookViewSet


router = DefaultRouter()

router.register(r"authors", AuthorViewSet)
router.register(r"genres", GenreViewSet)
router.register(r"libraries", LibraryViewSet)
router.register(r"books", BookViewSet)
