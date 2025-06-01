# forms.py
from django import forms
from .models import Student, Dataset
import re
from django import forms
import re
from .models import Student

import re
from django import forms
from .models import Student
from django.contrib.auth.models import User

class StudentProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )

    class Meta:
        model = Student
        fields = ['about', 'phone', 'profile_picture', 'skills', 'cv',
                  'google_scholar_profile', 'linkin_profile', 'github_profile']
        
        widgets = {
            'about': forms.Textarea(attrs={
                'name': 'body',
                'style': 'width:90%',
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[0-9]{11}',
                'title': 'Enter a valid 11-digit phone number'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'cv': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'application/pdf'
            }),
            'skills': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Separate skills with commas'
            }),
            'google_scholar_profile': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Google Scholar URL'
            }),
            'linkin_profile': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter LinkedIn URL'
            }),
            'github_profile': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter GitHub URL'
            }),
        }

        help_texts = {
            'phone': 'Enter an 11-digit phone number',
            'skills': 'Separate skills with commas (e.g., Python, Django, ML)',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        student = super().save(commit=False)
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            if commit:
                self.user.save()
        if commit:
            student.save()
            self.save_m2m()
        return student

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r'^\d{11}$', phone):
            raise forms.ValidationError('Enter a valid 11-digit phone number.')
        return phone

    def clean_skills(self):
        skills = self.cleaned_data.get('skills')
        if not skills or skills.strip() == "":
            raise forms.ValidationError('At least one skill is required.')
        return skills


    
from .models import News

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'image']
        

from django.forms import inlineformset_factory
from .models import Dataset, DatasetImage

class DatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['title', 'dataset_link', 'file', 'is_private']

# DatasetImageFormSet = inlineformset_factory(
#     Dataset,
#     DatasetImage,
#     fields=['image'],
#     extra=4,
#     max_num=4,
#     can_delete=True,
#     widgets={'image': forms.ClearableFileInput(attrs={'class': 'form-control'})}
# )