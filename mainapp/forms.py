from django import forms
from .models import Mainapp
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MainappForm(forms.ModelForm):
    class Meta:
        model=Mainapp
        fields=['text','photo']
        
class TextInputForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 80}), label='Enter your content')
    
    
    
class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=('username','email','password1','password2')