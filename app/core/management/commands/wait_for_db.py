"""
Django command to wait for the DB so the app can be connected
to the DB after that
"""
import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError

from psycopg2 import OperationalError as Psycog2Operror


class Command(BaseCommand):
    """
    Django command to wait for DB
    we will use BaseCommand as super class
    for accessing django base commands that
    can be run with manage.py on command line
    """

    def handle(self, *args, **options) -> str | None:
        """command Entrypoint"""
        self.stdout.write('waiting for database')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycog2Operror, OperationalError):
                self.stdout.write('database unavailable, waiting 1 second ..')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))
