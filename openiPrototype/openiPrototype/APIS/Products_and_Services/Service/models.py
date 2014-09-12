
__author__ = 'mpetyx'


from django.db import models
from OPENiapp.APIS.Context.models import OpeniContextAwareModel


class OpeniService(OpeniContextAwareModel):
    # id is missing because it is the default
    url = models.TextField()
    object_type = models.TextField()
    service = models.TextField()
    From = models.TextField()
    time = models.TextField()
    old_price = models.TextField()
    price = models.TextField()
    currency = models.TextField()
