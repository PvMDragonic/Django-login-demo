from django import forms
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        error_messages = {
            'username': {
                'required': "You must enter a username."
            },
            'email': {
                'required': "You must enter an email.",
                'invalid': "You must enter a valid email address."
            },
            'password': {
                'required': "You must enter a password."
            }
        }
        widgets = {
            'password': forms.PasswordInput()
        }

    def clean_password(self):
        password = self.cleaned_data['password']

        # Necessary for 'CustomStrictUserAttributeSimilarityValidator'.
        self.instance.username = self.cleaned_data.get('username', '') or self.instance.username
        self.instance.email = self.cleaned_data.get('email', '') or self.instance.email

        validate_password(password, user = self.instance)
        return password

    def save(self, commit = True):
        user = super().save(commit = False)
        user.password = make_password(self.cleaned_data['password']) 

        if commit:
            user.save()

        return user