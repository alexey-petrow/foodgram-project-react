from django.shortcuts import get_object_or_404
from rest_framework import serializers
# from rest_framework.relations import SlugRelatedField
from rest_framework.validators import (UniqueTogetherValidator,
                                       UniqueValidator)
from djoser.serializers import UserSerializer
from recipies.models import (Recipe, Ingredient, IngredientInRecipe, Tag,
                             User, Favorite, Subscription, Shoping_cart)


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            who_subscribes=self.context['request'].user.id,
            subscribes_to=obj.id
        ).exists()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurment_unit')
        # lookup_field = ('id')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient'
    )
    name = serializers.SerializerMethodField()
    measurment_unit = serializers.SerializerMethodField()

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurment_unit', 'amount')

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurment_unit(self, obj):
        return obj.ingredient.measurment_unit


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        # lookup_field = 'id'


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    ingredients = IngredientInRecipeSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        return Favorite.objects.filter(
            user=self.context['request'].user.id,
            recipe=obj.id
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        return Shoping_cart.objects.filter(
            user=self.context['request'].user.id,
            recipe=obj.id
        ).exists()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        new_recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            ingredient_in_recipe, create = (
                IngredientInRecipe.objects.get_or_create(**ingredient)
            )
            new_recipe.ingredients.add(ingredient_in_recipe)
        for tag in tags:
            new_recipe.tags.add(tag)
        return new_recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        instance.tags.clear()
        for tag in tags:
            instance.tags.add(tag)
        ingredients = validated_data.pop('ingredients')
        instance.ingredients.clear()
        for ingredient in ingredients:
            ingredient_in_recipe, create = (
                IngredientInRecipe.objects.get_or_create(**ingredient)
            )
            instance.ingredients.add(ingredient_in_recipe)
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.save()
        return instance

    validators = [
            UniqueTogetherValidator(
                queryset=Recipe.objects.all(),
                fields=('name', 'author'),
                message='Вы уже создавали такой рецепт.',
            )
        ]


class RecipeGetSerializer(RecipeSerializer):
    tags = TagSerializer(many=True)


class RecipePostSerializer(RecipeSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    # image = serializers.SerializerMethodField()
    cooking_time = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        # fields = ('id', 'name', 'image', 'cooking_time')
        fields = ('id', 'name', 'cooking_time')

    def get_id(self, obj):
        return obj.recipe.id

    def get_name(self, obj):
        return obj.recipe.name

    # def get_image(self, obj):
    #     return obj.recipe.image

    def get_cooking_time(self, obj):
        return obj.recipe.cooking_time
