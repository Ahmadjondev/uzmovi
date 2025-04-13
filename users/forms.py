from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help text
        for field in ['username', 'password1', 'password2']:
            self.fields[field].help_text = None

        # Make username not required
        self.fields['username'].required = False

        # Custom error messages in Uzbek
        self.fields['username'].error_messages = {
            'unique': 'Bu foydalanuvchi nomi allaqachon mavjud.',
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
        self.fields['password1'].label = 'Parol'
        self.fields['password2'].label = 'Parolni tasdiqlang'

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        # If username is not provided, generate one from email
        if not username and email:
            base_username = email.split('@')[0]
            username = base_username
            # Check if username exists and append numbers if needed
            suffix = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{suffix}"
                suffix += 1

            cleaned_data['username'] = username
            self.instance.username = username

        return cleaned_data

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(disabled=True, required=False)  # Make email read-only

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Custom error messages in Uzbek
        self.fields['username'].error_messages = {
            'unique': 'Bu foydalanuvchi nomi allaqachon mavjud.',
            'required': 'Foydalanuvchi nomini kiriting.',
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'dark_mode', 'email_notifications']

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
