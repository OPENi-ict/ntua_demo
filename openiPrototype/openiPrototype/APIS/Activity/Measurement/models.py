
__author__ = 'mpetyx'


from django.db import models
from OPENiapp.APIS.Context.models import OpeniContextAwareModel


class OpeniMeasurement(OpeniContextAwareModel):
    # id is missing because it is the default
    url = models.TextField()
    object_type = models.TextField()
    service = models.TextField()
    From = models.TextField()
    time = models.TextField()
    result = models.TextField()
    title = models.TextField()
    metric = models.TextField()
    text = models.TextField()
