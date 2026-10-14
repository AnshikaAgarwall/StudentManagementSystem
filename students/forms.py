from django import forms
from .models import Mark, ClassAssignment, StudentSubmission

class UpdateMarksForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['internal_marks', 'external_marks']
        widgets = {
            'internal_marks': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 30}),
            'external_marks': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 70}),
        }

class ClassAssignmentForm(forms.ModelForm):
    class Meta:
        model = ClassAssignment
        fields = ['title', 'description', 'assigned_class', 'due_date', 'reference_file']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class StudentSubmissionForm(forms.ModelForm):
    class Meta:
        model = StudentSubmission
        fields = ['submission_file', 'notes']
        widgets = {
            'submission_file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }