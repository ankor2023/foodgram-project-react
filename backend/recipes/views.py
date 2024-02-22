from rest_framework import filters, viewsets

from recipes.models import Recipe
from recipes.paginations import RecipePagination
from recipes.serializers import RecipeAddChangeSerializer, RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
#    serializer_class = RecipeAddChangeSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('^name', )


    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT'):
            return RecipeAddChangeSerializer
        return RecipeSerializer

