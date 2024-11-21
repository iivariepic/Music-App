from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


class Album(models.Model):
    """A model for albums"""
    name = models.CharField(max_length=300)
    release_year = models.IntegerField(default=1900,
                    validators=[
                        MaxValueValidator(datetime.datetime.now().year()), 
                        MinValueValidator(1900)])