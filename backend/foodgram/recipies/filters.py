from foodgram.filters import Filter
from django_filters import rest_framework
from .models import Recipe, Favorite, ShoppingCart, Tag
from rest_framework.filters import SearchFilter


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
    tags = rest_framework.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = rest_framework.BooleanFilter(
        field_name='is_favorited', method='filter_is_favorited')
    is_in_shopping_cart = rest_framework.BooleanFilter(
        field_name='is_in_shopping_cart', method='filter_is_in_shopping_cart')

    # Надо делать функцию так как методы одинаковые
    def filter_is_favorited(self, queryset, name, value):
        favorits = Favorite.objects.filter(
            user=self.request.user.id)
        recipes_list = [favorite.recipe.id for favorite in favorits]
        if value == 1:
            return Recipe.objects.filter(id__in=recipes_list)
        return Recipe.objects.all().exclude(id__in=recipes_list)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        items_in_shopping_cart = ShoppingCart.objects.filter(
            user=self.request.user.id)
        recipes_list = [item.recipe.id for item in items_in_shopping_cart]
        if value == 1:
            return Recipe.objects.filter(id__in=recipes_list)
        return Recipe.objects.all().exclude(id__in=recipes_list)

    class Meta:
        fields = ('author',)
        model = Recipe
