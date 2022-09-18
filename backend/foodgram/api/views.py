from collections import namedtuple

from django.http import HttpResponse
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action

from recipies.filters import IngredientSearchFilter, RecipeFilter
from recipies.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .pagination import LimitPageNumberPagination
from .permissions import IsAdminAuthorOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeGetSerializer, RecipePostSerializer,
                          ShoppingCartSerializer, TagSerializer)
from .utils import create_and_delete_relation, ingredients_list_to_pdf


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAdminAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = LimitPageNumberPagination

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
            FavoriteSerializer,
            part_of_error_message='избранном')

    @action(
        methods=['post', 'delete'],
        detail=True,
        url_path='shopping_cart')
    def shopping_cart(self, request, pk=None):
        return create_and_delete_relation(
            request, pk,
            ShoppingCart,
            ShoppingCartSerializer,
            part_of_error_message='списке покупок')

    @action(
        methods=['get'],
        detail=False,
        url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        ingredients_list = ShoppingCart.objects.filter(
            user=request.user
        ).values_list(
            'recipe__ingredients__ingredient__name',
            'recipe__ingredients__ingredient__measurement_unit'
        ).annotate(total_amount=Sum(
            'recipe__ingredients__amount', distinct=True)
        )
        Ing = namedtuple('Ing', ['name', 'measurement_unit', 'total_amount'])
        ingredients_namedtuples_list = []
        for ingredient in ingredients_list:
            ingredients_namedtuples_list.append(
                Ing(name=ingredient[0],
                    measurement_unit=ingredient[1],
                    total_amount=ingredient[2])
            )
        pdf_file = ingredients_list_to_pdf(ingredients_namedtuples_list)
        content_type = 'application/pdf'
        return HttpResponse(pdf_file, content_type=content_type)
