
__author__ = 'mpetyx'

from django.db import models
from OPENiapp.APIS.Context.models import OpeniContextAwareModel


class OpeniVideo(OpeniContextAwareModel):
    # id is missing because it is the default
    url = models.TextField()
    object_type = models.TextField()
    service = models.TextField()
    From = models.TextField()
    File = models.TextField()
    duration = models.TextField()
    Time = models.TextField()
    tags = models.TextField()
    text = models.TextField()