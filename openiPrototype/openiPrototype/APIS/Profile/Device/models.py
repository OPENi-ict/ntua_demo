
__author__ = 'mpetyx'


from django.db import models
from OPENiapp.APIS.Context.models import OpeniContextAwareModel


class OpeniDevice(OpeniContextAwareModel):
    # id is missing because it is the default
    url = models.TextField()
    object_type = models.TextField()
    service = models.TextField()
    From = models.TextField()
    profile = models.TextField()