# Generated by Django 3.2.3 on 2024-02-19 04:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_alter_tag_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=7, null=True, validators=[django.core.validators.RegexValidator(message='Цвет должен быть задан 16-ричным числом (например: #E26C2D)', regex='^#[a-fA-F0-9]{1,6}$')], verbose_name='Цвет'),
        ),
    ]