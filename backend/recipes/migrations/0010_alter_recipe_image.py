# Generated by Django 3.2.3 on 2024-02-27 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_alter_recipe_cooking_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='recipes/', verbose_name='Картинка'),
        ),
    ]
