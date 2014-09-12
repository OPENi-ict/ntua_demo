
__author__ = 'mpetyx'


from django.db import models
from OPENiapp.APIS.Context.models import OpeniContextAwareModel

class OpeniAccount(OpeniContextAwareModel):
    # id is missing because it is the default
    url = models.TextField()
    object_type = models.TextField()
    service = models.TextField()
    From = models.TextField()
    Time = models.TextField()
    Person = models.TextField()
    wallet = models.TextField()
    user = models.TextField()
    username = models.TextField()
    email = models.TextField()
    password = models.TextField()
    validated = models.BooleanField()
    active = models.BooleanField()
