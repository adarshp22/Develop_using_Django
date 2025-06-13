from django import forms
from .models import Mainapp, SEOAnalysis
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# ---------------------------------------------
# Form for the Mainapp model
# Used to collect text and optional image from the user
# ---------------------------------------------
class MainappForm(forms.ModelForm):
    class Meta:
        model = Mainapp
        fields = ['text', 'photo']  # Only include fields for user input


# ---------------------------------------------
# Form for SEOAnalysis model
# Used to submit text to the backend for SEO analysis
# ---------------------------------------------
class SEOForm(forms.ModelForm):
    class Meta:
        model = SEOAnalysis
        fields = ['input_text']  # Only the input text is needed from the user

        # Customizing the textarea widget to be more user-friendly
        widgets = {
            'input_text': forms.Textarea(attrs={
                'rows': 10,  # Number of visible text lines
                'cols': 80,  # Width of the text area
                'placeholder': 'Enter your blog, caption, or content here...'
            }),
        }


# ---------------------------------------------
# Custom user registration form using Django's built-in UserCreationForm
# Includes email field along with username and password fields
# ---------------------------------------------
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()  # Make email a required field

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  # Fields to display in form
