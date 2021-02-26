from django import forms
from django.forms import Form, ModelForm

from .models import Family, FitnessRecord


class FitnessRecordForm(ModelForm):
    class Meta:
        model = FitnessRecord
        fields = ['category', 'calories', 'duration']

class CreateFamilyForm(ModelForm):
    class Meta:
        model = Family
        fields = ['name']

        widgets = {
            'members': forms.CheckboxSelectMultiple
        }

class JoinFamilyForm(Form):
    code = forms.CharField(label='Family Code', min_length=6, max_length=6)
