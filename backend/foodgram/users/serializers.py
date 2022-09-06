from rest_framework import serializers
from djoser.serializers import UserSerializer
from .models import User, Subscription
from recipies.models import Recipe


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


class LiteRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        # fields = ('id', 'name', 'image', 'cooking_time')
        fields = ('id', 'name', 'cooking_time')


class SubscribeSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='subscribes_to.email')
    id = serializers.ReadOnlyField(source='subscribes_to.id')
    username = serializers.ReadOnlyField(source='subscribes_to.username')
    first_name = serializers.ReadOnlyField(source='subscribes_to.first_name')
    last_name = serializers.ReadOnlyField(source='subscribes_to.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        return True

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(
            author=obj.subscribes_to)
        serializer = LiteRecipeSerializer(queryset, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.subscribes_to.recipies.count()

    class Meta:
        model = Subscription
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
