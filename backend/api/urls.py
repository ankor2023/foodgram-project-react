from django.urls import include, path
from rest_framework.routers import DefaultRouter




urlpatterns = [
    path('users/', include('users.urls')),
    path('tags/', include('tags.urls')),
    path('ingredients/', include('ingredients.urls')),
    path('recipes/', include('recipes.urls')),
]

