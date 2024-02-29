import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from ingredients.models import Ingredient, Unit


class Command(BaseCommand):
    """Command to load data from csv files to DB."""

    help = 'Load ingredients and measurement units data from .csv to DB'

    def handle(self, *args, **options):
        print(f'Use path: {options["path"]}')

        filename = 'ingredients.csv'
        print(f'Load file {filename}')
        with open(f'{options["path"]}/{filename}') as f:
            reader = csv.reader(f)
            for ingredient_name, unit_name in reader:
                print(ingredient_name)
                unit, status = Unit.objects.get_or_create(name=unit_name)
                print(unit)
                Ingredient.objects.get_or_create(name=ingredient_name,
                                                 measurement_unit=unit)

        return 'OK'

    def add_arguments(self, parser):
        parser.add_argument(
            '-p',
            '--path',
            action='store',
            default=str(settings.BASE_DIR) + '/initial_data',
            help='Path to .csv files',
        )
