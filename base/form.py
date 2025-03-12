# forms.py
from django import forms
from .models import Student
import re

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['about','phone', 'profile_picture', 'skills']
        widgets = {
            'about':forms.Textarea(
                attrs={
                    'name':'body',
                    'style':'width:90%'
                }
            )
            ,
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[0-9]{11}',
                'title': '11-digit phone number'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        help_texts = {
            'phone': 'Enter 11-digit phone number',
            'skills': 'Separate skills with commas',
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r'^[0-9]{11}$', phone):
            raise forms.ValidationError('Enter a valid 11-digit phone number')
        return phone

    def clean_skills(self):
        skills = self.cleaned_data.get('skills')
        if not skills:
            raise forms.ValidationError('At least one skill is required')
        return skills