from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'favorite_genres', 'dark_mode', 'email_notifications']
        widgets = {
            'favorite_genres': forms.CheckboxSelectMultiple(),
            'bio': forms.Textarea(attrs={'rows': 3}),
        }
