from django.db import models

from backend import settings

class Unit(models.Model):
    name = models.CharField('Название', max_length=settings.CHAR_FIELD_MAX_LEN, unique=True)
    full_name = models.CharField('Полное название', max_length=settings.CHAR_FIELD_MAX_LEN, null=True)
    
    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=settings.CHAR_FIELD_MAX_LEN, unique=False)
    measurement_unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name='ingredients', verbose_name='Единица измерения'
    )
    

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique_ingredient'),
        )

    def __str__(self):
        return self.name
