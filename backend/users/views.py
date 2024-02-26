from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from subscriptions.models import Subscription
from subscriptions.serializers import SubscriptionSerializer
from users.serializers import PasswordSerializer, UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    @action(('get',), detail=False, permission_classes=(IsAuthenticated,))
    def me(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)


    @action(("post",), detail=False, permission_classes=(IsAuthenticated,))
    def set_password(self, request, *args, **kwargs):
        serializer = PasswordSerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)

        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(("post",'delete'), detail=True, permission_classes=(IsAuthenticated,))
    def subscribe(self, request, *args, **kwargs):
        author = get_object_or_404(User, id=kwargs['pk'])
        user = request.user

        if request.method == 'POST':
            if user == author:
                return Response({'errors': 'Попытка подписаться на самого себя.'}, status=status.HTTP_400_BAD_REQUEST)
                #raise serializers.ValidationError('Попытка подписаться на самого себя.')
            if Subscription.objects.filter(user=user, author=author):
                return Response({'errors': f'Вы уже подписаны на {author.username}.'}, status=status.HTTP_400_BAD_REQUEST)
                #raise serializers.ValidationError(f'Вы уже подписаны на {author.username}.')

            subscription = Subscription(user=user, author=author)
            serializer = SubscriptionSerializer(subscription, context={'request': request})
            subscription.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            get_object_or_404(Subscription, user=user, author=author).delete()
            return Response({'detail': 'OK'}, status=status.HTTP_204_NO_CONTENT)


