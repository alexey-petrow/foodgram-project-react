from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipies.models import Recipe
from .models import Subscription, User


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


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class RecipeForSubcribeSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


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
        return Subscription.objects.filter(
            who_subscribes=self.context['request'].user.id,
            subscribes_to=obj.subscribes_to.id
        ).exists()

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(
            author=obj.subscribes_to)[:3]
        request = self.context['request']
        serializer = RecipeForSubcribeSerializer(
            queryset,
            many=True,
            context={'request': request})
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
