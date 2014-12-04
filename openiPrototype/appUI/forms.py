__author__ = 'alvertisjo'
from django.forms import ModelForm,forms, DateInput
from appUI.models import Person, AgeGroup

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ['gender', 'educationalLevel','birthday','children', 'married','income','interests', 'country','ethnicity']


class AgeGroupForm(ModelForm):
    class Meta:
        model = AgeGroup
        fields = ['ageGroup']