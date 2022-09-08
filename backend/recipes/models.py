from django.core.validators import MinValueValidator
from django.db import models

from tags.models import Tag
from users.models import CustomUser


class Ingredient(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name='Название ингредиента',
        help_text='Введите название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Название единицы измерения',
        help_text='Введите название единицы измерения',
    )

    class Meta:
        verbose_name = 'Ингредиенты'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
        help_text='Введите автора рецепта',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Введите название рецепта',
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Фотография блюда',
        help_text='Добавьте фотографию блюда',
    )
    text = models.CharField(
        max_length=20000,
        verbose_name='Описание рецепта',
        help_text='Введите описание рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='ingredients',
        through='IngredientAmount',
        verbose_name='Ингредиенты',
        help_text='Выберите необходимые ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        verbose_name='Тег',
        help_text='Введите теги для рецепта',
    )
    cooking_time = models.PositiveIntegerField(
        null=False,
        validators=(
            MinValueValidator(
                1,
                'Время приготовления не может быть меньше одной минуты',
            ),
        ),
        verbose_name='Время приготовления',
        help_text='Укажите время приготовления',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='amounts',
        verbose_name='Ингредиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='amounts',
        verbose_name='Рецепт',
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество ингредиента',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'ingredient',
                    'recipe',
                ),
                name='unique_dish',
            ),
        )
        verbose_name = 'Количество ингредиента для рецепта'
        verbose_name_plural = 'Количество ингредиентов для рецепта'

    def __str__(self):
        return f'{self.recipe} - {self.ingredient}'


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorites_user',
        verbose_name='Избранные рецепты',
        help_text='Избранные рецепты пользователя',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites_recipe',
        verbose_name='Избранные рецепты у пользователей',
        help_text='Избранные рецепты у пользователей',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'user',
                    'recipe',
                ),
                name='unique_favorites',
            ),
        )
        verbose_name = 'Избранные рецепты'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'{self.user} added {self.recipe} to favorite list'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Список покупок',
        help_text='Список покупок пользователя',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Корзина покупок',
        help_text='Ингредиенты в списке покупок пользователя',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'user',
                    'recipe',
                ),
                name='unique_recipe',
            ),
        )
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.user} added {self.recipe} to shopping cart'
