from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
from .models import Agreement, SkillListing
from .models import Review
from .models import Agreement
from django import forms
from .models import SkillListing


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'location', 'video_intro_url', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['bio', 'location', 'video_intro_url', 'profile_image']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'video_intro_url': forms.URLInput(attrs={'class': 'form-control'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }






class AgreementForm(forms.ModelForm):
    accept_terms = forms.BooleanField(
        required=True,
        label='',  # Suppress default label
        widget=forms.CheckboxInput(attrs={'id': 'accept_terms'})
    )

    class Meta:
        model = Agreement
        fields = ['responder', 'requested_skill', 'start_date', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional message or expectations...'}),
        }




class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=True
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']


class SkillListingForm(forms.ModelForm):
    class Meta:
        model = SkillListing
        fields = ['skill', 'description', 'is_offer']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe this skill...'}),
            'skill': forms.Select(attrs={'class': 'form-select'}),
            'is_offer': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'is_offer': 'I am offering this skill',
        }
