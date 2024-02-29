from django.contrib import admin

from ingredients.models import Unit, Ingredient

admin.site.register(Unit)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', )
    list_filter = ('name', )
    search_fields = ('name',)
