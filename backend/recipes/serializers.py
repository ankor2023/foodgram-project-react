import base64
from pprint import pprint

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from ingredients.serializers import IngredientSerializer
from recipes.models import Ingredient, Recipe, RecipeIngredient
from tags.models import Tag
from tags.serializers import TagSerializer




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


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(source='ingredients_in_recipe', read_only=True, many=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Recipe
        fields = '__all__'

class RecipeAddChangeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSimpleSerializer(source='ingredients_in_recipe', many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Recipe
        fields = ('name', 'ingredients', 'cooking_time', 'tags')


    def create(self, validated_data):

        ingredients = validated_data.pop('ingredients_in_recipe')
        tags = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)
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
