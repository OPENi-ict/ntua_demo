__author__ = 'mpetyx'

from django.contrib import admin
from .models import OpeniContext


class ContextAdmin(admin.ModelAdmin):
    pass

admin.site.register(OpeniContext, ContextAdmin)
