from OPENiapp.APIS.Context.models import OpeniContextAwareModel

__author__ = 'mpetyx'


from django.db import models


class OpeniStatus(OpeniContextAwareModel):
    # id is missing because it is the default
    url = models.TextField()
    object_type = models.TextField()
    service = models.TextField()
    From = models.TextField()
    time = models.TextField()
    text = models.TextField()
    title = models.TextField()
