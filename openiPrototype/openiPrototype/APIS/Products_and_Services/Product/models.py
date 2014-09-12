from OPENiapp.APIS.Context.models import OpeniContextAwareModel

__author__ = 'mpetyx'


from django.db import models


class OpeniProduct(OpeniContextAwareModel):
    # id is missing because it is the default
    url = models.TextField()
    object_type = models.TextField()
    service = models.TextField()
    From = models.TextField()
    price = models.TextField()
    currency = models.TextField()
    amount = models.TextField()
    code = models.TextField()
    profile = models.TextField()
