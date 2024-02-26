from django.urls import include, path
from rest_framework.routers import DefaultRouter




urlpatterns = [
    path('users/subscriptions/', include('subscriptions.urls')),
    path('users/', include('users.urls')),
    path('tags/', include('tags.urls')),
    path('ingredients/', include('ingredients.urls')),
    path('recipes/', include('recipes.urls')),
#    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

