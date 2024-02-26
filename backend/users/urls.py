from django.urls import include, path
from rest_framework.routers import DefaultRouter

from subscriptions.views import SubscriptionViewSet
from users.views import UserViewSet

router = DefaultRouter()

router.register('', UserViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls)),

]

