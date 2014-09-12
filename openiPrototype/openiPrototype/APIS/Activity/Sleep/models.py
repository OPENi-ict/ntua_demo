from OPENiapp.APIS.Context.models import OpeniContextAwareModel

__author__ = 'mpetyx'


from django.db import models


class OpeniSleep(OpeniContextAwareModel):
    # id is missing because it is the default
    url = models.TextField()
    object_type = models.TextField()
    service = models.TextField()
    From = models.TextField()
    duration = models.TextField()
    deep = models.TextField()
    rem = models.TextField()
    light = models.TextField()
    awake = models.TextField()
    times_woken = models.TextField()
