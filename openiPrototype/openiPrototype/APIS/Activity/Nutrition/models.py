
__author__ = 'mpetyx'


from django.db import models
from OPENiapp.APIS.Context.models import OpeniContextAwareModel


class OpeniNutrition(OpeniContextAwareModel):
    # id is missing because it is the default
    url = models.TextField()
    object_type = models.TextField()
    service = models.TextField()
    From = models.TextField()
    meal = models.TextField()
    calories = models.TextField()
    fat = models.TextField()
    fiber = models.TextField()
    protei  = models.TextField()
    sodium = models.TextField()
    water = models.TextField()
