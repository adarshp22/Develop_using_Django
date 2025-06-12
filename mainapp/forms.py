from django import forms
from .models import Mainapp,SEOAnalysis
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MainappForm(forms.ModelForm):
    class Meta:
        model=Mainapp
        fields=['text','photo']
        

class SEOForm(forms.ModelForm):
    class Meta:
        model = SEOAnalysis
        fields = ['input_text']
        widgets = {
            'input_text': forms.Textarea(attrs={'rows': 10, 'cols': 80}),
        }
    
    
    
class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=('username','email','password1','password2')