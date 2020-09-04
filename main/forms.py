from django import forms
from django.forms import Form, ModelForm
from .models import FitnessRecord

class FitnessRecordForm(ModelForm):
    class Meta:
        model = FitnessRecord
        fields = ['category', 'calories', 'duration']
