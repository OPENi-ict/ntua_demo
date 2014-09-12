__author__ = 'mpetyx'

from django.contrib import admin
from .models import OpeniOrder


class OrderAdmin(admin.ModelAdmin):
    pass


admin.site.register(OpeniOrder, OrderAdmin)
