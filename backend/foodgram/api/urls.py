from rest_framework import routers
from django.urls import include, path

from .views import (TagViewSet, IngredientViewSet,
                    RecipeViewSet,)

router = routers.DefaultRouter()
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'ingredients', IngredientViewSet, basename='ingredient')
router.register(r'recipes', RecipeViewSet, basename='recipe')


urlpatterns = [
    path('', include(router.urls)),
]
