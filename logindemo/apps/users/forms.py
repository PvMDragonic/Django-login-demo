from django import forms
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm

class CustomUserForm(forms.ModelForm):
    # Outside Meta because it's not saved to the database.
    password_repeat = forms.CharField(
        label = "Repeat password",
        widget = forms.PasswordInput(),
        required = True
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email']
        error_messages = {
            'username': {
                'required': "You must enter a username."
            },
            'password': {
                'required': "You must enter a password."
            },
            'email': {
                'required': "You must enter an email.",
                'invalid': "You must enter a valid email address."
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
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_repeat = cleaned_data.get('password_repeat')

        if password and password_repeat and password != password_repeat:
            self.add_error('password_repeat', "Passwords do not match.")

        return cleaned_data

    def save(self, commit = True):
        user = super().save(commit = False)
        user.password = make_password(self.cleaned_data['password']) 

        if commit:
            user.save()

        return user
    
class CustomPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        # Removes the 'is_active = True' default check.
        active_users = get_user_model()._default_manager.filter(
            email__iexact = email
        )

        return (
            user for user in active_users if user.has_usable_password()
        )