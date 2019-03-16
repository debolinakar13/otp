from django import forms
from .models import User

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone', 'email', 'first_name','last_name','gender']

class AuthenticationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone']

class OTPForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['otp']
