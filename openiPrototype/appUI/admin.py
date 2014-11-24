from django.contrib import admin

# Register your models here.

from models import *

class VenueCategories(admin.ModelAdmin):
    pass
admin.site.register(VenueCategory, VenueCategories)

class Venues(admin.ModelAdmin):
    pass
admin.site.register(Venue, Venues)

class Checkins(admin.ModelAdmin):
    pass
admin.site.register(Checkin, Checkins)

class Persons(admin.ModelAdmin):
    pass
admin.site.register(Person, Persons)

class Ratings(admin.ModelAdmin):
    pass
admin.site.register(Rating, Ratings)