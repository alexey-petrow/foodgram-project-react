from django.contrib import admin

from .models import (Recipe, Ingredient, Tag, IngredientInRecipe,
                     Favorite, Subscription, Shopping_cart)

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(IngredientInRecipe)
admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(Subscription)
admin.site.register(Shopping_cart)
