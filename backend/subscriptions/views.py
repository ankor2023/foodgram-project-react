from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from subscriptions.models import Subscription
from subscriptions.serializers import SubscriptionSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        return self.request.user.authors.all()


