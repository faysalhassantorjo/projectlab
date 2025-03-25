# forms.py
from django import forms
from .models import Student, Dataset
import re
from django import forms
import re
from .models import Student

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['about', 'phone', 'profile_picture', 'skills', 'cv', 'google_scholar_profile', 'linkin_profile', 'github_profile']
        
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
        

class DatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['title', 'dataset_link', 'file', 'is_private']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply MDB styling to each field
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'style': 'rows:10',
            'placeholder': 'Enter dataset title',
        })
        self.fields['dataset_link'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter dataset link (optional)',
        })
        self.fields['file'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['is_private'].widget.attrs.update({
            'class': 'form-check-input',
        })

        # Add labels with MDB styling
        self.fields['title'].label = 'Title'
        self.fields['dataset_link'].label = 'Dataset Link'
        self.fields['file'].label = 'Upload File'
        self.fields['is_private'].label = 'Private Dataset'