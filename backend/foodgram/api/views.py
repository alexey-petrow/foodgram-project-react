from rest_framework import viewsets, permissions, filters, status
# from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response

from recipies.models import (Recipe, Ingredient, Tag, User,
                             Favorite, Subscription, Shoping_cart)
from .permissions import IsAdminAuthorOrReadOnly
from .mixins import CreateDestroyViewSet
from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeGetSerializer, RecipePostSerializer,
                          FavoriteSerializer)


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


class FavoriteViewSet(CreateDestroyViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('recipe_id'))
        serializer.save(user=user, recipe=recipe)

    # @action(methods=['delete'], detail=False)
    # def delete_from_favorits(self, request, pk=None):
    #     user = request.user
    #     recipe = get_object_or_404(Recipe, id=self.kwargs.get('recipe_id'))
    #     instance = Favorite.objects.filter(user=user, recipe=recipe)
    #     instance.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
