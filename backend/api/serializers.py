from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (
    Favorite,
    Ingredient,
    IngredientAmount,
    Recipe,
    ShoppingCart,
)
from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import CustomUserSerializer


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class GetRecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(
        source='amounts',
        read_only=True,
        many=True,
    )
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    cooking_time = serializers.IntegerField(min_value=1)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'pub_date',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'cooking_time',
            'text',
        )

    def get_ingredients(self, obj):
        queryset = IngredientAmount.objects.filter(recipe=obj)
        return IngredientAmountSerializer(queryset, many=True).data

    def get_favorited(self, obj):
        return getattr(obj, 'is_favorited', False)

    def get_shopping_cart(self, obj):
        return getattr(obj, 'is_in_shopping_cart', False)

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=request.user, recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj).exists()


class AddIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount',)


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = AddIngredientSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    @staticmethod
    def create_ingredients(ingredients, recipe):
        for ingredient in ingredients:
            IngredientAmount.objects.create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )

    @staticmethod
    def create_tags(tags, recipe):
        for tag in tags:
            recipe.tags.add(tag)

    def create(self, validated_data):
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
        author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.create_tags(tags, recipe)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        IngredientAmount.objects.filter(recipe=instance).delete()
        self.create_tags(validated_data.pop('tags'), instance)
        self.create_ingredients(validated_data.pop('ingredients'), instance)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return GetRecipeSerializer(instance, context=context).data


class SimpleRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        recipe = data['recipe']
        if Favorite.objects.filter(user=request.user, recipe=recipe).exists():
            raise serializers.ValidationError({
                'status': 'Вы уже добавили этот рецепт в избранное'
            })
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return SimpleRecipeSerializer(
            instance.recipe,
            context=context
        ).data


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = (
            'user',
            'recipe',
        )

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return SimpleRecipeSerializer(
            instance.recipe, context=context).data
