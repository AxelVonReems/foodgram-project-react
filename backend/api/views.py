import csv

from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsOwnerOrReadOnly
from api.serializers import (
    FavoriteSerializer,
    GetRecipeSerializer,
    IngredientSerializer,
    RecipeSerializer,
    ShoppingCartSerializer
)
from recipes.models import (
    Ingredient,
    Favorite,
    Recipe,
    ShoppingCart
)
from api.paginators import CustomPageNumberPaginator


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsOwnerOrReadOnly,)
    ordering = ('-pub_date',)
    pagination_class = CustomPageNumberPaginator

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return GetRecipeSerializer
        return RecipeSerializer

    @staticmethod
    def actions_post(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def actions_delete(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_obj = get_object_or_404(model, user=user, recipe=recipe)
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST'],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        return self.actions_post(
            request=request, pk=pk,
            serializers=FavoriteSerializer
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.actions_delete(
            request=request, pk=pk, model=Favorite
        )

    @action(
        detail=True,
        methods=['POST'],
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        return self.actions_post(
            request=request, pk=pk, serializers=ShoppingCartSerializer
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.actions_delete(
            request=request, pk=pk, model=ShoppingCart)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        shopping_cart = Recipe.objects.filter(
            shopping_cart__user=request.user
        ).order_by('ingredients__name').values(
            'ingredients__name', 'ingredients__measurement_unit'
        ).annotate(total_quantity=Sum('amounts__amount'))

        response = HttpResponse(content_type='txt/csv')
        response['Content-Disposition'] = (
            'attachment; filename=shopping_list.txt'
        )
        writer = csv.writer(response)

        for item in shopping_cart:
            writer.writerow([
                f"{item['ingredients__name']} - "
                f"({item['total_quantity']} "
                f"{item['ingredients__measurement_unit']})"
            ])
        return response
