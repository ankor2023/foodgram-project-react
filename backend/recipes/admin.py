from django.contrib import admin

from recipes.models import Recipe, RecipeIngredient, RecipeTag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display =  ('name', )
    list_filter = ('name', 'tags', )
    filter_horizontal = ('ingredients', )

@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display =  ('recipe', 'ingredient', 'amount')

@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'tag')

