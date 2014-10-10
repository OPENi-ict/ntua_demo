__author__ = 'alvertisjo'
from django.forms import ModelForm,forms, DateInput
from appUI.models import Person

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ['gender', 'educationalLevel','birthday','children', 'married','income','interests']
        widgets = {
            'birthday': DateInput(attrs={'class':'datepicker'}),
        }


