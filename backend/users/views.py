from django.contrib.auth import get_user_model
from django.db import models
from rest_framework import viewsets

from users.serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
