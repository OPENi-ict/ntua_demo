from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Person(models.Model):
    GENDER = (
    ('M', 'male'),
    ('F', 'female'),
    )
    EDU = (
    ('Primary', 'Primary'),
    ('Secondary', 'Secondary'),
    ('College', 'College'),
    ('Bachelor', 'Bachelor'),
    ('MSc', 'Masters'),
    ('PhD', 'Doctorate'),
    )
    CHILDREN = (
    ('0', 'no children'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('M', 'more than 4'),
    )
    MARRIED = (
    (True, 'Yes'),
    (False, 'No')
    )
    #user = models.ForeignKey(User,related_name="%(app_label)s_%(class)s_related")
    fsq_user_id = models.CharField("User ID",max_length=100, null=True, blank=True)
    gender= models.CharField("Gender*",max_length=1, choices=GENDER,null=False)
    educationalLevel=models.CharField("Education Level*",max_length=20, choices=EDU,null=False)
    birthday=models.DateField("Birth date (YYYY-MM-DD)*",blank=False,null=False)
    children= models.CharField("Number of children",max_length=10,choices=CHILDREN,null=True,blank=True)
    married = models.BooleanField("Married",choices=MARRIED,blank=True)
    income= models.FloatField("Yearly income in euro",null=True,blank=True)
    interests = models.CharField(max_length=400, null=True, blank=True)
    def setFsqID(self, id):
        self.fsq_user_id=id
    class Meta:
        verbose_name_plural = "Persons"
    def __unicode__(self):
        return "pk=%d ,  fsq_user_id=%s, gender=%s" % (self.pk,self.fsq_user_id, self.gender)


class Venue (models.Model):
    service_id = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    lat= models.FloatField("Yearly income",null=True,blank=True)
    lng = models.FloatField("Yearly income",null=True,blank=True)
    cc= models.CharField(max_length=100, null=True, blank=True)
    city= models.CharField(max_length=100, null=True, blank=True)
    state= models.CharField(max_length=100, null=True, blank=True)
    country= models.CharField(max_length=100, null=True, blank=True)
    class Meta:
        verbose_name_plural = "Venues"
    def __unicode__(self):
        return "pk=%d , name= %s ,lat=%s, lng=%s, city=%s, country=%s " % (self.pk,self.name, self.lat, self.lng,self.city, self.country)

class VenueCategory (models.Model):
    service_id = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    venue= models.ForeignKey(Venue,related_name="%(app_label)s_%(class)s_related")
    class Meta:
        verbose_name_plural = "Venue Categories"
    def __unicode__(self):
        return "pk=%d , name= %s ,venue=%s " % (self.pk,self.name, self.venue)


class Checkin (models.Model):
    service_id = models.CharField(max_length=100, null=True, blank=True)
    service  = models.CharField(max_length=100, null=True, blank=True)
    createdAt = models.BigIntegerField(null=False,blank=False)
    createdBy  = models.ForeignKey(Person,related_name="%(app_label)s_%(class)s_related")
    venue = models.ForeignKey(Venue,related_name="%(app_label)s_%(class)s_related")
    class Meta:
        verbose_name_plural = "Check-ins"
    def __unicode__(self):
        return "pk=%d , service= %s ,venue=%s, createdAt=%s " % (self.pk,self.service, self.venue.name, self.createdAt)


class Rating (models.Model):
    product_id = models.CharField(max_length=100, null=False, blank=False)
    rate = models.FloatField(null=False,blank=False)
    createdBy  = models.ForeignKey(Person,related_name="%(app_label)s_%(class)s_related")
    class Meta:
        verbose_name_plural = "Ratings"
    def __unicode__(self):
        return "pk=%d , product= %s ,rate=%s, createdBy=%s " % (self.pk,self.product_id, self.rate, self.createdBy)

