from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ingredients.views import IngredientViewSet

router = DefaultRouter()

router.register('', IngredientViewSet, basename='ingredient')


urlpatterns = [
    path('', include(router.urls)),

]

