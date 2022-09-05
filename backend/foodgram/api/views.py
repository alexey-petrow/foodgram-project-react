from rest_framework import viewsets, permissions, filters, status
# from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response

from recipies.models import (Recipe, Ingredient, Tag, User,
                             Favorite, Subscription, Shopping_cart)
from .permissions import IsAdminAuthorOrReadOnly
from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeGetSerializer, RecipePostSerializer,
                          FavoriteAndShoppingCartSerializer)
from .utils import create_and_delete_relation


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
        if self.request.method == 'GET':
            return RecipeGetSerializer
        return RecipePostSerializer

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

    @action(
        methods=['post', 'delete'],
        detail=True,
        url_path='favorite')
    def favorite(self, request, pk=None):
        return create_and_delete_relation(
            request, pk,
            Favorite,
            FavoriteAndShoppingCartSerializer,
            part_of_error_message='избранном')

    @action(
        methods=['post', 'delete'],
        detail=True,
        url_path='shopping_cart')
    def shopping_cart(self, request, pk=None):
        return create_and_delete_relation(
            request, pk,
            Shopping_cart,
            FavoriteAndShoppingCartSerializer,
            part_of_error_message='списке покупок')
