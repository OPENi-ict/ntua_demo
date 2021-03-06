from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

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
    INCOME=(
        (1, '<5,000'),
        (2, '5,000-9,999'),
        (3, '10,000-14,999'),
        (4, '15,000-19,999'),
        (5, '20,000-24,999'),
        (6, '25,000-29,999'),
        (7, '30,000-34,999'),
        (8, '35,000-49,999'),
        (9, '50,000-150,000'),
        (10, '>150,000'),
    )
    MARRIED = (
    (True, 'Yes'),
    (False, 'No')
    )
    #user = models.ForeignKey(User,related_name="%(app_label)s_%(class)s_related")
    fsq_user_id = models.CharField("User ID",max_length=100, null=True, blank=True)
    gender= models.CharField("Gender*",max_length=1, choices=GENDER,null=False)
    educationalLevel=models.CharField("Education Level*",max_length=20, choices=EDU,null=False)
    birthday=models.DateField("Birth date (YYYY-MM-DD)*",blank=True,null=False)
    children= models.CharField("Number of children",max_length=10,choices=CHILDREN,null=True,blank=True)
    married = models.BooleanField("Married",choices=MARRIED,blank=True, default=False)
    income= models.FloatField("Yearly income in euro",choices=INCOME, default=None, null=True,blank=True)
    interests = models.CharField(help_text="A comma separated list, e.g. 'shopping, soccer, swimming'",max_length=400, null=True, blank=True)
    country=CountryField("Country*", help_text="The country of residence")
    ethnicity=CountryField("Ethnicity*", help_text="The country you come from")
    def setFsqID(self, id):
        self.fsq_user_id=id
    class Meta:
        verbose_name_plural = "Persons"
    def __unicode__(self):
        return "pk=%d ,  fsq_user_id=%s, gender=%s" % (self.pk,self.fsq_user_id, self.gender)

class AgeGroup(models.Model):
    AGE = (
    (1, '13-17'),
    (2, '18-24'),
    (3, '25-34'),
    (4, '35-44'),
    (5, '45-54'),
    (6, '55-64'),
    (7, '65+'),
    )
    person=models.ForeignKey(Person,related_name="%(app_label)s_%(class)s_related")
    ageGroup=models.IntegerField("Age Group*",choices=AGE, blank=False,null=False)
    class Meta:
        verbose_name_plural = "AgeGroups"
    def __unicode__(self):
        return "pk=%d ,  person=%s, gender=%s" % (self.pk,self.person, self.ageGroup)


class Venue (models.Model):
    service_id = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    lat= models.FloatField("Yearly income",null=True,blank=True)
    lng = models.FloatField("Yearly income",null=True,blank=True)
    cc= models.CharField(max_length=100, null=True, blank=True)
    city= models.CharField(max_length=200, null=True, blank=True)
    state= models.CharField(max_length=200, null=True, blank=True)
    country= models.CharField(max_length=200, null=True, blank=True)
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

