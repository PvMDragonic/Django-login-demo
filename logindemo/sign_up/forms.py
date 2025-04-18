from django import forms
from .models import CustomUser
from django.contrib.auth.hashers import make_password

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self, commit = True):
        user = super().save(commit = False)
        user.password = make_password(self.cleaned_data['password']) 

        if commit:
            user.save()

        return user