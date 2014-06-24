"""
Management command to clear specified app's models of data.

.. moduleauthor:: Infoxchange Development Team <development@infoxchange.net.au>

"""

from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from django.db import connection
from django.db.models import get_app, get_model, get_models
from south.db import db

# pylint:disable=protected-access


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
                if verbosity >= 1:
                    print "Found %d model(s) for %s" % (len(app_models), app)

        db.start_transaction()

        for model in models:
            if verbosity >= 1:
                print "Clearing %s table %s" % (model, model._meta.db_table)
            db.clear_table(model._meta.db_table)
            sql = connection.ops.sequence_reset_sql(no_style(), [model])
            for cmd in sql:
                connection.cursor().execute(cmd)

        db.commit_transaction()

        if verbosity >= 1:
            print "Cleared %d models" % len(models)
