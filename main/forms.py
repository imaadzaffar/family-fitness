from django import forms
from django.forms import Form, ModelForm

from .models import Family, FitnessRecord


class FitnessRecordForm(ModelForm):
    class Meta:
        model = FitnessRecord
        fields = ['category', 'calories', 'duration']

class FamilyForm(ModelForm):
    class Meta:
        model = Family
        fields = ['name']

        widgets = {
            'members': forms.CheckboxSelectMultiple
        }
