import json

from django.core.management.base import BaseCommand, CommandError

from list_auto.models import Brand, CarModel


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        brand = Brand.objects.get(pk=1)
        with open('translated_kia.json', 'r', encoding='utf8') as file:
            content = file.read()
            options = json.loads(content)
            for key in options:
                print(key)
                opt_in_dict = CarModel.objects.filter(name__exact=key['label'])
                if not  opt_in_dict:
                    opt = CarModel(name=key['label'], korea_name=key['name'], code=key['code'], brand=brand)
                    opt.save()
                    print(key)
