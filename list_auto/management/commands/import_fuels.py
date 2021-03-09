import json

from django.core.management.base import BaseCommand, CommandError

from list_auto.models import Color, TransmissionsType, GasolineType


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        with open('translated_fuels.json', 'r', encoding='utf8') as file:
            content = file.read()
            options = json.loads(content)
            for key in options:
                opt_in_dict = GasolineType.objects.filter(name__exact=key['label'])
                if not  opt_in_dict:
                    opt = GasolineType(name=key['label'], korea_name=key['name'], code=key['code'])
                    opt.save()
                    print(key)
