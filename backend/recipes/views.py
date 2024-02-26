from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


from recipes.filters import RecipeFilter
from recipes.models import Recipe, UserFavorite, UserShoppingCart
from recipes.permissions import IsOwnerOrReadOnly
from recipes.serializers import RecipeAddChangeSerializer, RecipeSerializer, RecipeSimpleSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    search_fields = ('^name', )
    filterset_class = RecipeFilter



    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return RecipeAddChangeSerializer
        return RecipeSerializer

    @action(('post', 'delete'), detail=True, permission_classes=(IsAuthenticated,))
    def favorite(self, request, **kwargs):
        user = request.user
        recipe = get_object_or_404(Recipe, id=kwargs['pk'])

        if request.method == 'POST':

            if UserFavorite.objects.filter(user=user, recipe=recipe):
                return Response({'errors': f'Рецепт {recipe} уже в избранном.'}, status=status.HTTP_400_BAD_REQUEST)
            UserFavorite.objects.create(user=user, recipe=recipe)
            serializer = RecipeSimpleSerializer(recipe)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            get_object_or_404(UserFavorite, user=user, recipe=recipe).delete()
            return Response({'detail': 'OK'}, status=status.HTTP_204_NO_CONTENT)


    @action(('post', 'delete'), detail=True, permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, **kwargs):
        user = request.user
        recipe = get_object_or_404(Recipe, id=kwargs['pk'])

        if request.method == 'POST':

            if UserShoppingCart.objects.filter(user=user, recipe=recipe):
                return Response({'errors': f'Рецепт {recipe} уже в списке покупок.'}, status=status.HTTP_400_BAD_REQUEST)
            UserShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = RecipeSimpleSerializer(recipe)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            get_object_or_404(UserShoppingCart, user=user, recipe=recipe).delete()
            return Response({'detail': 'OK'}, status=status.HTTP_204_NO_CONTENT)

