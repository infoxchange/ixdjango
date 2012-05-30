"""
Models for ixdjango app
"""
from django.db import models


class TestModel(models.Model):
    """
    A dummy model to get django test framework to pick up the app. Can be
    removed once the app has real models
    (see: https://code.djangoproject.com/ticket/7198)
    """
    pass
