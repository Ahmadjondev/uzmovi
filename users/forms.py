from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField(
        required=True,  # Make username required but not unique
        help_text="Enter your name (this doesn't need to be unique)"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help text
        for field in ['password1', 'password2']:
            self.fields[field].help_text = None

        # Custom error messages in Uzbek
        self.fields['username'].error_messages = {
            'required': 'Ismingizni kiriting.',
        }

        self.fields['password1'].error_messages = {
            'required': 'Iltimos, parolni kiriting',
            'min_length': 'Parol kamida 8 ta belgidan iborat bo\'lishi kerak',
            'password_too_short': 'Parol juda qisqa. Kamida 8 ta belgidan iborat bo\'lishi kerak.',
        }

        self.fields['password2'].error_messages = {
            'required': 'Parolni tasdiqlang',
            'password_mismatch': 'Ikkala parol bir xil emas.',
        }

        # Custom labels
        self.fields['username'].label = 'Ismingiz'
        self.fields['password1'].label = 'Parol'
        self.fields['password2'].label = 'Parolni tasdiqlang'

    def clean_username(self):
        """
        Override the unique username validation.
        We'll still validate other aspects of the username.
        """
        username = self.cleaned_data.get('username')
        # We're not checking for uniqueness here
        return username


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(disabled=True, required=False)  # Make email read-only

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Custom error messages in Uzbek
        self.fields['username'].error_messages = {
            'required': 'Ismingizni kiriting.',
        }

        # Custom labels
        self.fields['username'].label = 'Ismingiz'


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['dark_mode', 'email_notifications']


class EmailVerificationForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tasdiqlash kodi'}),
        error_messages={
            'required': 'Tasdiqlash kodini kiriting',
            'min_length': 'Kod 6 raqamdan iborat bo\'lishi kerak',
            'max_length': 'Kod 6 raqamdan iborat bo\'lishi kerak',
        }
    )
