
__author__ = 'mpetyx'


from django.db import models
from OPENiapp.APIS.Context.models import OpeniContextAwareModel


class OpeniCard(OpeniContextAwareModel):
    # id is missing because it is the default
    url = models.TextField()
    object_type = models.TextField()
    service = models.TextField()
    From = models.TextField()
    billing_address = models.TextField()
    number = models.TextField()
    card_owner_date_of_birth = models.TextField()
    card_type = models.TextField()
    expiration_date = models.TextField()
    card_verification_number = models.TextField()
