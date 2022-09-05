from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингредиента',
        max_length=200,
        unique=True
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200
    )

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT
    )
    amount = models.SmallIntegerField(
        'Количество',
        validators=[
            MinValueValidator(1),
        ]
    )


class Tag(models.Model):
    name = models.CharField(
        'Название тега',
        max_length=200,
        unique=True
    )
    color = models.CharField(
        'Цвет тега',
        max_length=7,
        null=True
    )
    slug = models.SlugField(
        max_length=200,
        unique=True
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    tags = models.ManyToManyField(
        Tag,
        related_name='recipies'
    )
    ingredients = models.ManyToManyField(
        IngredientInRecipe,
        related_name='recipies'
    )
    cooking_time = models.SmallIntegerField(
        'Время приготовления в минутах',
        validators=[
            MinValueValidator(1),
        ]
    )
    text = models.TextField('Текст рецепта')
    image = models.ImageField(
        upload_to='recipies/',
        null=True,
        blank=True
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='recipies',
        null=True
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorits'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorits'
    )

    def __str__(self):
        return f'Рецепт {self.recipe.name} в избранном у {self.user.username}.'


class Subscription(models.Model):
    who_subscribes = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribes',
        verbose_name='Тот кто подписывается'
    )
    subscribes_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Тот на кого подписываются'
    )


class Shopping_cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping'
    )
