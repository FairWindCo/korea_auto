import json
import os

import googletrans
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError

from importer.report_processor import get_images_counts, process_report_file
from list_auto.models import Brand, CarModel, CarVersion, TransmissionsType, GasolineType, Color, Car, CarOptions


def translate(text, translator, dest='en'):
    translated = translator.translate(text, src='ko', dest=dest)
    # print('TRANSLATE: ', text, translated.text)
    return translated.text


def get_car_foreign_object(korea_name, db_table, translator, korea_code=-1, **kwargs):
    default_value = {}
    if kwargs:
        default_value.update(kwargs)
    default_value.update({
        'korea_name': korea_name,
        'code': korea_code,
    })
    db_object, created = db_table.objects.get_or_create(korea_name=korea_name, defaults=default_value)
    if db_object:
        if created:
            db_object.name = translate(korea_name, translator)
            db_object.save()
        return db_object
    return None


def process_options_list(list_options, translator):
    result = []
    for option in list_options:
        opt = get_car_foreign_object(option, CarOptions, translator)
        if opt:
            result.append(opt)
    return result


def get_car_json(path, dir, file_name='car_data.json'):
    file_path = os.path.abspath(os.path.join(path, dir, file_name))
    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            with open(file_path, 'r', encoding='utf8') as file:
                return json.loads(file.read())
        except Exception as e:
            print(f'ERROR in file {file_name} {e}')
    else:
        print(f'ERROR NO file {file_name}  in {dir}')
    return None


def process_additional_info(path, dir, translator):
    file_path = os.path.abspath(os.path.join(path, dir, 'detail.html'))
    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            with open(file_path, 'r', encoding='utf8') as file:
                content = file.read()
                options = []
                soup = BeautifulSoup(content, 'html.parser')
                div_detail = soup.find('div', id='ui_popup_cardetail')
                options_li = div_detail.find_all('li')
                for option_li in options_li:
                    label = option_li.find('label')
                    if 'class' in label.attrs and 'checked' in label.attrs['class']:
                        options.append(label.text)
                price = soup.find('strong', id='ui_ViewCarAmount')

                return options, price.text.replace(',', '').replace('.', '') if price else None
        except Exception as e:
            print(f'ERROR in detail.html dir {dir} {e}')
    else:
        print(f'ERROR NO  detail.html in {dir}')
    return [], None


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
                car_json = get_car_json(path, dir)
                if car_json:
                    car = None
                    created = False
                    try:
                        car = Car.objects.get(car_code=dir)
                    except Car.DoesNotExist:
                        car = Car()
                        created = True
                        car.car_code = car_json['CarNo']
                        car.mileage = int(car_json['CarUseKm'])
                        car.year = int(car_json['CarRegYear'])
                        car.car_LPG_use = bool(car_json['CarLPGUseYn'])
                        car.plate_number = car_json['CarPlateNumber']
                        car.jesi_no = car_json['CarJesiNo']
                        car.price_dealer = int(car_json['CarAmountDealer'])
                        car.price_sale = int(car_json['CarAmountSale'])
                        car.checkout_no = car_json['CarCheckoutNo']
                        car.price = 0
                    if car:
                        if created:
                            car_brand = get_car_foreign_object(car_json['CarMakerName'], Brand, translator)
                            car_model = get_car_foreign_object(car_json['CarModelDetailName'], CarModel, translator, -1,
                                                               brand=car_brand)
                            car_model_version = get_car_foreign_object(car_json['CarGradeName'], CarVersion, translator,
                                                                       -1,
                                                                       model_version=car_model)
                            transmission = get_car_foreign_object(car_json['CarMission'], TransmissionsType, translator)
                            fuel = get_car_foreign_object(car_json['CarFuel'], GasolineType, translator)
                            color = get_car_foreign_object(car_json['CarColor'], Color, translator)
                            car.gasoline = fuel
                            car.transmission = transmission
                            car.color = color
                            car.model_version = car_model_version
                            big_images, small_images = get_images_counts(path, dir)
                            car.image_count = big_images
                            car.label_image_count = small_images
                            vin, reg_date, _, _ = process_report_file(path, dir, translator)
                            car.vin_number = vin
                            car.first_register_date = reg_date
                            car.save()
                            options = process_options_list(car_json['CarOption'].split(','), translator)
                            for option in options:
                                car.options.add(option)
                            additional, price = process_additional_info(path, dir, translator)
                            car.price = int(price)
                            options = process_options_list(additional, translator)
                            for option in options:
                                car.options.add(option)
                            car.save()
                    else:
                        print('ERROR IN PROCESS', car_json)
                else:
                    print('ERROR IN PROCESS DIR ', dir)
        else:
            raise CommandError('No DataBase dir')
