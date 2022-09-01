from rest_framework import routers
from django.urls import include, path

from .views import TagViewSet, IngredientViewSet, RecipeViewSet, UserViewSet, IngredientInRecipeViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'ingredients', IngredientViewSet, basename='ingredient')
# router.register(r'ingredients_in_recipe', IngredientInRecipeViewSet, basename='ingredient_in_recipe')
router.register(r'recipes', RecipeViewSet, basename='recipe')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.authtoken')),
]
