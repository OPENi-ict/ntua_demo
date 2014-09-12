
__author__ = 'mpetyx'


from django.db import models
from OPENiapp.APIS.Context.models import OpeniContextAwareModel


class OpeniWorkout(OpeniContextAwareModel):
    # id is missing because it is the default
    url = models.TextField()
    object_type = models.TextField()
    service = models.TextField()
    From = models.TextField()
    Location = models.TextField()
    duration = models.TextField()
    text = models.TextField()
    equipment = models.TextField()
    distance = models.TextField()
    metric = models.TextField()
    previous_id = models.TextField()
    next_id = models.TextField()
