"""
Management command to clear specified app's models of data.

.. moduleauthor:: Infoxchange Development Team <development@infoxchange.net.au>

"""

from __future__ import print_function

from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from django.db import connection, transaction
# pylint:disable=no-name-in-module
from django.db.models import get_app, get_model, get_models

# pylint:disable=protected-access


real_print = print  # pylint:disable=invalid-name


def print(*args, **kwargs):  # pylint:disable=redefined-builtin
    """
    Only print if required
    """

    if kwargs.pop('verbosity') >= 1:
        real_print(*args, **kwargs)


class Command(BaseCommand):
    """
    A command to clear app data.
    """

    help = ('Cleans the specified applications\' tables to a pristine state.')

    def handle(self, *targets, **options):
        verbosity = int(options['verbosity'])

        models = []
        for target in targets:
            target = target.split('.')

            try:
                app, = target
                model = None
            except ValueError:
                app, model = target

            if model:
                models.append(get_model(app, model))
            else:
                app_models = [
                    model
                    for model
                    in get_models(get_app(app), include_auto_created=True)
                    if model._meta.managed
                ]
                models += app_models
                print("Found %d model(s) for %s" % (len(app_models), app),
                      verbosity=verbosity)

        with transaction.atomic():
            for model in models:
                print("Clearing %s table %s" % (
                      model, model._meta.db_table),
                      verbosity=verbosity)

                cursor = connection.cursor()
                cursor.execute('TRUNCATE TABLE {} CASCADE'.format(
                    model._meta.db_table))

                sql = connection.ops.sequence_reset_sql(no_style(), [model])
                for cmd in sql:
                    connection.cursor().execute(cmd)

        print("Cleared %d models" % len(models), verbosity=verbosity)
