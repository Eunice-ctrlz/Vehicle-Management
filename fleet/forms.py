from django import forms
from .models import ConditionReport, MechanicRequest


class ConditionReportForm(forms.ModelForm):
    class Meta:
        model = ConditionReport
        fields = ['description', 'photo']


class MechanicRequestForm(forms.ModelForm):
    class Meta:
        model = MechanicRequest
        fields = ['issue_description']