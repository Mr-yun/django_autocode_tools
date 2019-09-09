from __future__ import print_function

from django.core.management.base import BaseCommand
from django_crontab.crontab import Crontab

from django_autocode_tools.auto_code import AutoCode


class Command(BaseCommand):
    help = '''
    add: automatically add restful api and basic orm operation.
    remove: remove automatic add script.
    refresh: refreshes serialized file'''

    def add_arguments(self, parser):
        parser.add_argument('subcommand', choices=['add',  'remove','refresh'],
                            help=self.help)
        parser.add_argument('jobhash', nargs='?')

    def handle(self, *args, **options):
        auto = AutoCode(**options)
        if options['subcommand'] == 'add':
            auto.add()
        elif options['subcommand'] == 'remove':
            auto.remove()
        elif options['subcommand'] == 'refresh':
            auto.refresh()
        else:
            print(self.help)
