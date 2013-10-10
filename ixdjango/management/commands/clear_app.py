"""
Management command to clear specified app's models of data.

.. moduleauthor:: Infoxchange Development Team <development@infoxchange.net.au>

"""

from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from django.db import connection
from django.db.models import get_app, get_models
from south.db import db

# pylint:disable=protected-access

class Command(BaseCommand):
    """
    A command to clear app data.
    """

    def handle(self, *apps, **options):
        models = []
        for app in apps:
            app_models = [
                model
                for model
                in get_models(get_app(app), include_auto_created=True)
                if model._meta.managed
            ]
            models += app_models
            print "Found %d model(s) for %s" % (len(app_models), app)

        db.start_transaction()

        for model in models:
            print "Clearing %s table %s" % (model, model._meta.db_table)
            db.clear_table(model._meta.db_table)
            sql = connection.ops.sequence_reset_sql(no_style(), [model])
            for cmd in sql:
                connection.cursor().execute(cmd)

        db.commit_transaction()

        print "Cleared %d models" % len(models)
