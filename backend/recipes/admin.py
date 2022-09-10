from django.contrib import admin

from recipes.models import (
    Favorite,
    Ingredient,
    IngredientAmount,
    Recipe,
    ShoppingCart,
)


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)
    search_fields = ('name', 'measurement_unit',)
    empty_value_display = '-пусто-'


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    min_num = 1
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'name',
        'image',
        'text',
    )
    search_fields = (
        'name',
        'author__username',
        'author__email',
    )
    list_filter = (
        'author',
        'name',
        'tags',
    )
    inlines = (RecipeIngredientInline,)
    empty_value_display = '-пусто-'


class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'recipe',
        'ingredient',
        'amount',
    )
    search_fields = (
        'user__username',
        'user__email',
        'recipe__name',
    )
    empty_value_display = '-пусто-'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',
    )
    search_fields = (
        'user__username',
        'user__email',
        'recipe__name',
    )
    empty_value_display = '-пусто-'


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',
    )
    search_fields = (
        'user__username',
        'user__email',
        'recipe__name',
    )
    empty_value_display = '-пусто-'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
