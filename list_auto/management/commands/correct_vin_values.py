import json
import os

import googletrans
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError

from importer.report_processor import get_images_counts, process_report_file
from list_auto.models import Brand, CarModel, CarVersion, TransmissionsType, GasolineType, Color, Car, CarOptions

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--file_database_dir', type=str, dest='database_dir', default='./DataBase/')

    def handle(self, *args, **options):
        translator = googletrans.Translator()
        path = options['database_dir']
        if os.path.exists(path) and os.path.isdir(path):
            dirs = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
            for dir in dirs:
                vin, reg_date, year, drive = process_report_file(path, dir, translator)
                try:
                    car = Car.objects.get(car_code=dir)
                except Car.DoesNotExist:
                    print(f'CAR Num: {dir} not exists')
                    continue
                if car.vin_number is None:
                    car.vin_number = vin
                    car.first_register_date = reg_date
                    car.save()
        else:
            raise CommandError('No DataBase dir')
