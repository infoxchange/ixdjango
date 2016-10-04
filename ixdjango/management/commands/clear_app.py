"""
Management command to clear specified app's models of data.

.. moduleauthor:: Infoxchange Development Team <development@infoxchange.net.au>

"""

from __future__ import print_function

from django.apps import apps
from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from django.db import connection, transaction

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
    args = '<app_label> <app_label> ... '

    def handle(self, *targets, **options):
        """
        Clear the data for the given apps.
        """
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
                models.append(apps.get_model(app, model))
            else:
                app_models = self.get_managed_models_for_app(app)
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

    def get_models_module(self, app):
        """
        Return the models module for the given app.
        """

        return apps.get_models(apps.get_app_config(app).models_module, True)

    def get_managed_models_for_app(self, app):
        """
        Return a list of managed models for the given app.
        """

        return [
            model for model in self.get_models_module(app)
            if model._meta.managed
        ]
