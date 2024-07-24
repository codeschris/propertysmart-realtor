from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import User, Profile

class UserRegistrationForm(UserCreationForm):
    email_address = forms.EmailField(max_length=255, required=True, help_text='Required. Provide a valid email address.')
    phone_number = forms.CharField(max_length=50, required=True)
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, required=True)

    bio = forms.CharField(widget=forms.Textarea, required=True)
    address = forms.CharField(max_length=255, required=True)
    preferences = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = User
        fields = ['name', 'email_address', 'phone_number', 'password1', 'password2', 'user_type']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register', css_class='btn btn-primary btn-block'))

class LoginForm(AuthenticationForm):
    email_address = forms.EmailField(max_length=255, required=True, help_text='Required. Enter a valid email address.')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Login', css_class='btn btn-primary'))

    def clean(self):
        # Optional: Add custom validation if needed
        return super().clean()