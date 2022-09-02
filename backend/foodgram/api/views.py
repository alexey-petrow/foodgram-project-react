from rest_framework import viewsets, permissions, filters
# from rest_framework.pagination import LimitOffsetPagination
# from django.shortcuts import get_object_or_404

from recipies.models import (Recipe, Ingredient, Tag, User,
                             Favorite, Subscription, Shoping_cart)
from .permissions import IsAdminAuthorOrReadOnly
# from .mixins import ListCreateViewSet
from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeGetSerializer, RecipePostSerializer,)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAdminAuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RecipeGetSerializer
        return RecipePostSerializer

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)
