from django import forms
from .models import Mark, Assignment

class UpdateMarksForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['internal_marks', 'external_marks']

class UpdateAssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['is_submitted']