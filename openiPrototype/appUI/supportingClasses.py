__author__ = 'alvertisjo'

from datetime import datetime
from django.http import HttpResponseRedirect

class OPENiAuthorization:
    def checkIfExpired(self, tokenCreatedDatetime):
        last_activity = tokenCreatedDatetime
        now = datetime.now()

        if (now - last_activity).days <=1:
            # Do logout / expire session
            # and then...
            return True
        else:
            return False

