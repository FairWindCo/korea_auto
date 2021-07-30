from django.core.management.base import BaseCommand

from importer.main_import_procedure import import_car_data
from korea_auto import settings


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--pages', type=int, dest='max_page', default=1)
        parser.add_argument('--file_database_dir', type=str, dest='database_dir', default='./DataBase/')
        parser.add_argument('--user', type=str, dest='user', default=settings.KOREA_SITE_USER)
        parser.add_argument('--pass', type=str, dest='password', default=settings.KOREA_SITE_PASS)
        parser.add_argument('--par_page', type=int, dest='peg_page', default=10)
        parser.add_argument('--region', type=int, dest='region', default=103)
        parser.add_argument('--area', type=int, dest='area', default=1035)
        parser.add_argument('--donji', type=int, dest='donji', default=94001)
        parser.add_argument('--brand', type=int, dest='brand', default=None)
        parser.add_argument('--model', type=int, dest='model', default=None)
        parser.add_argument('--proxy', type=str, dest='proxy', default=None)

    def handle(self, *args, **options):
        import_car_data(options['user'],
                        options['password'],
                        options['database_dir'],
                        options['max_page'],
                        options['peg_page'],
                        options['region'],
                        options['area'],
                        options['donji'],
                        options['brand'],
                        options['model'],
                        options['proxy']
                        )
