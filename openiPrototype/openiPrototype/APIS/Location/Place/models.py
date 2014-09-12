
__author__ = 'mpetyx'


from django.db import models
from OPENiapp.APIS.Context.models import OpeniContextAwareModel


class OpeniEvent(OpeniContextAwareModel):
    # id is missing because it is the default
    url = models.TextField()
    object_type = models.TextField()
    service = models.TextField()
    From = models.TextField()
    place = models.TextField()
    text = models.TextField()

