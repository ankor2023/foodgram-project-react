import base64
from pprint import pprint

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from ingredients.serializers import IngredientSerializer
from recipes.models import Ingredient, Recipe, RecipeIngredient, UserFavorite, UserShoppingCart
from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import UserSerializer




class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)

class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit.name')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)

class RecipeIngredientSimpleSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source='ingredient.id', queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount',)

class RecipeSimpleSerializer(serializers.ModelSerializer):
    """Only for subscriptions, favorites and shopping cart display."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')



class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(source='ingredients_in_recipe', read_only=True, many=True)
    tags = TagSerializer(read_only=True, many=True)

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'


    def get_is_favorited(self, obj):
        if not self.context:
            return False
        user = self.context.get('request').user
        return user.is_authenticated and UserFavorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        if not self.context:
            return False
        user = self.context.get('request').user
        return user.is_authenticated and UserShoppingCart.objects.filter(user=user, recipe=obj).exists()


class RecipeAddChangeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientSimpleSerializer(source='ingredients_in_recipe', many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Recipe
        fields = ('name', 'text', 'ingredients', 'image', 'cooking_time', 'tags', 'author')


    def create(self, validated_data):

        ingredients = validated_data.pop('ingredients_in_recipe')
        tags = validated_data.pop('tags')

        recipe = Recipe.objects.create(author=self.context['request'].user, **validated_data)
        for ingredient in ingredients:
            current_ingredient = ingredient['ingredient']['id']
            RecipeIngredient.objects.create(recipe=recipe, ingredient=current_ingredient, amount=ingredient['amount'])

        recipe.tags.set(tags)

        return recipe

    def update(self, instance, validated_data):

        ingredients = validated_data.pop('ingredients_in_recipe')
        tags = validated_data.pop('tags')
        instance.ingredients.clear()
        instance.tags.clear()

        for ingredient in ingredients:
            current_ingredient = ingredient['ingredient']['id']
            RecipeIngredient.objects.get_or_create(recipe=instance, ingredient=current_ingredient, amount=ingredient['amount'])

        instance.tags.set(tags)

        return super().update(instance, validated_data)



    def to_representation(self, value):
        return RecipeSerializer(value).data

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError({'ingredients': 'Пустой список.'})

        if len(value) != len(set([ingredient['ingredient']['id'].id for ingredient in value])):
            raise serializers.ValidationError({'ingredients': 'Значения должны быть уникальны.'})

        return value

    
    def validate_tags(self, value):
        if not value:
            raise serializers.ValidationError({'tags': 'Пустой список.'})

        if len(value) != len(set([tag.id for tag in value])):
            raise serializers.ValidationError({'tags': 'Значения должны быть уникальны.'})

        return value

    def validate(self, obj):
        for field in ('name', 'text', 'cooking_time', 'image', 'tags', 'ingredients_in_recipe'):
            if not obj.get(field):
                raise serializers.ValidationError({f'{field}': 'Поле обязательно.'})

        return obj
