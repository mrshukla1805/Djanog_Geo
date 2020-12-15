from django import forms
from .models import Measures

class MeasurementModelForm(forms.ModelForm):
    class Meta:
        model = Measures
        fields = ('destination',)