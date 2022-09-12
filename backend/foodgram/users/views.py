from rest_framework import status
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import User, Subscription
from .serializers import SubscribeSerializer


class CustomUserViewSet(UserViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @action(
        methods=['get'],
        detail=False,
        url_path='subscriptions')
    def subscriptions(self, request):
        queryset = Subscription.objects.filter(
            who_subscribes=request.user)
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubscribeSerializer(
                page,
                many=True,
                context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = SubscribeSerializer(
            queryset,
            many=True,
            context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['post', 'delete'],
        detail=True,
        url_path='subscribe')
    def subscribe(self, request, id=None):
        who_subscribes = request.user
        subscribes_to = get_object_or_404(User, id=id)
        is_relation_exists = Subscription.objects.filter(
            who_subscribes=who_subscribes,
            subscribes_to=subscribes_to).exists()
        if request.method == 'POST':
            if is_relation_exists:
                return Response(
                    {'errors':
                        (f'Вы уже подписаны на пользователя'
                         f' {subscribes_to.username}!')},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif who_subscribes == subscribes_to:
                return Response(
                    {'errors':
                        ('Подписываться на самого себя'
                         'запрещено!')},
                    status=status.HTTP_400_BAD_REQUEST
                )
            instance = Subscription.objects.create(
                who_subscribes=who_subscribes,
                subscribes_to=subscribes_to)
            serializer = SubscribeSerializer(
                instance, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            if not is_relation_exists:
                return Response(
                    {'errors':
                        (f'Вы не подписаны на пользователя'
                         f'{subscribes_to.username}!')},
                    status=status.HTTP_400_BAD_REQUEST
                )
            instance = get_object_or_404(
                Subscription,
                who_subscribes=who_subscribes,
                subscribes_to=subscribes_to)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
