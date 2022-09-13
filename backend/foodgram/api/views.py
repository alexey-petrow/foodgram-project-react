from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action

from recipies.filters import IngredientSearchFilter, RecipeFilter
from recipies.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .permissions import IsAdminAuthorOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeGetSerializer, RecipePostSerializer,
                          ShoppingCartSerializer, TagSerializer)
from .utils import create_and_delete_relation, ingredients_dict_to_pdf


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
        shopping_cart = ShoppingCart.objects.filter(
            user=request.user)
        recipes_list = [instance.recipe for instance in shopping_cart]
        ingredients_list = []
        for recipe in recipes_list:
            ingredients = recipe.ingredients.all()
            for ingredient in ingredients:
                ingredients_list.append(
                    (ingredient.ingredient.name,
                     ingredient.ingredient.measurement_unit,
                     ingredient.amount))
        ing_set = set(f'{item[0]} ({item[1]})' for item in ingredients_list)
        ing_list = list(ing_set)
        ing_dict = dict.fromkeys(sorted(ing_list), 0)
        for ingredient in ingredients_list:
            ing_dict[f'{ingredient[0]} ({ingredient[1]})'] += ingredient[2]
        pdf_file = ingredients_dict_to_pdf(ing_dict)
        content_type = 'application/pdf'
        return HttpResponse(pdf_file, content_type=content_type)
