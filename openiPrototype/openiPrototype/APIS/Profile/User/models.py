from OPENiapp.APIS.Context.models import OpeniContextAwareModel

__author__ = 'mpetyx'


from django.db import models


class OpeniUser(OpeniContextAwareModel):
    # id is missing because it is the default
    url = models.TextField()
    object_type = models.TextField()
    service = models.TextField()
    url_to_original_user = models.TextField()