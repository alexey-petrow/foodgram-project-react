from django_filters import rest_framework
from rest_framework.filters import SearchFilter

from foodgram.filters import Filter
from .models import Favorite, Recipe, ShoppingCart, Tag


class NameFilter(Filter):
    title = 'названию'
    parameter_name = 'name'


class UsernameFilter(Filter):
    title = 'имени автора'
    parameter_name = 'author__username'


class TagnameFilter(Filter):
    title = 'названию тега'
    parameter_name = 'tags__name'


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(rest_framework.FilterSet):
    author = rest_framework.NumberFilter(field_name='author__id')
    is_favorited = rest_framework.BooleanFilter(
        field_name='is_favorited', method='filter_is_favorited')
    is_in_shopping_cart = rest_framework.BooleanFilter(
        field_name='is_in_shopping_cart', method='filter_is_in_shopping_cart')
    tags = rest_framework.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    def filter_is_favorited(self, queryset, name, value):
        recipes_list = Favorite.objects.filter(
            user=self.request.user.id).values_list('recipe__id', flat=True)
        if value == 1:
            return Recipe.objects.filter(id__in=recipes_list)
        return Recipe.objects.all().exclude(id__in=recipes_list)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        recipes_list = ShoppingCart.objects.filter(
            user=self.request.user.id).values_list('recipe__id', flat=True)
        if value == 1:
            return Recipe.objects.filter(id__in=recipes_list)
        return Recipe.objects.all().exclude(id__in=recipes_list)

    class Meta:
        fields = ('author',)
        model = Recipe
