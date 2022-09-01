from rest_framework import viewsets, permissions, filters
# from rest_framework.pagination import LimitOffsetPagination
# from django.shortcuts import get_object_or_404

from recipies.models import (Recipe, Ingredient, Tag, User,
                             IngredientInRecipe,
                             Favorite, Subscription, Shoping_cart)
# from .permissions import AuthorOrReadOnly
# from .mixins import ListCreateViewSet
from .serializers import (TagSerializer, IngredientSerializer,
                          IngredientInRecipeSerializer,
                          RecipeGetSerializer, RecipePostSerializer,
                          CustomUserSerializer)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class IngredientInRecipeViewSet(viewsets.ModelViewSet):
    queryset = IngredientInRecipe.objects.all()
    serializer_class = IngredientInRecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RecipeGetSerializer
        return RecipePostSerializer

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)
