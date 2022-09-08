from django_filters import (
    FilterSet, AllValuesMultipleFilter, CharFilter
)
from django_filters import rest_framework as filters

from recipes.models import Recipe, Ingredient


class IngredientFilter(FilterSet):
    name = CharFilter(
        field_name='name',
        lookup_expr='istartswith',
    )

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    tags = AllValuesMultipleFilter(
        field_name='tags__slug',
    )
    is_favorited = filters.BooleanFilter(
        method='get_is_favorited',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart',
    )

    class Meta:
        model = Recipe
        fields = (
            'author',
            'tags',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(favorites_recipe__user=user)
        return Recipe.objects.all()

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(shopping_cart__user=user)
        return Recipe.objects.all()
