from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help text
        for field in ['username', 'password1', 'password2']:
            self.fields[field].help_text = None

        # Custom error messages for password
        self.fields['password1'].error_messages = {
            'required': 'Please enter a password',
            'min_length': 'Password must be at least 8 characters long',
        }

        # Custom labels
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'

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
