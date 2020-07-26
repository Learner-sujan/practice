from django import forms
from .models import record

class uploadForm(forms.Form):
    Profile = forms.ImageField()
    
class loginForm(forms.Form):
    Username = forms.CharField(help_text='Username must be unique')
    Password = forms.CharField(help_text='must be more than 5 characters',widget=forms.PasswordInput)

