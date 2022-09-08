from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from api.paginators import CustomPageNumberPaginator
from users.models import Following, CustomUser
from users.serializers import CustomUserSerializer, FollowingSerializer


class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowingViewSet(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPaginator
    serializer_class = FollowingSerializer

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        if user_id == request.user.id:
            return Response(
                {'error': 'Нельзя подписываться на себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Following.objects.filter(
                user=request.user,
                author_id=user_id,
        ).exists():
            return Response(
                {'error': 'Вы уже подписаны на этого пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        author = get_object_or_404(CustomUser, id=user_id)
        Following.objects.create(
            user=request.user,
            author_id=user_id,
        )
        return Response(
            self.serializer_class(author, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        get_object_or_404(CustomUser, id=user_id)
        subscription = Following.objects.filter(
            user=request.user,
            author_id=user_id
        )
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Вы не подписаны на данного пользователя'},
            status=status.HTTP_400_BAD_REQUEST
        )


class FollowingListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPaginator
    serializer_class = FollowingSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(following__user=self.request.user)
