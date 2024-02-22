from django.db import models

from backend import settings
from ingredients.models import Ingredient
from tags.models import Tag

class Recipe(models.Model):
    name = models.CharField('Название', max_length=settings.CHAR_FIELD_MAX_LEN)
    text = models.TextField('Описание')
    cooking_time = models.PositiveSmallIntegerField('Время приготовления')
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    tags = models.ManyToManyField(Tag, through='RecipeTag')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ingredients_in_recipe', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField('Количество', null=False, default=1)

    class Meta:
        verbose_name = 'Ингридиента рецепта'
        verbose_name_plural = 'Ингридиенты рецепта'

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'

class RecipeTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Таг рецепта'
        verbose_name_plural = 'Таги рецепта'

    def __str__(self):
        return f'{self.recipe} {self.tag}'

