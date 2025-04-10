from django import forms
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'favorite_genres', 'dark_mode', 'email_notifications']
        widgets = {
            'favorite_genres': forms.CheckboxSelectMultiple(),
            'bio': forms.Textarea(attrs={'rows': 3}),
        }
