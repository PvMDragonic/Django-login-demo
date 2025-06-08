from django.contrib.auth import authenticate, logout
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib import messages

from config.utils import handle_login

def home(request):
    return render(request, 'landing/home.html')

def dashboard_login(request):
    if request.method == 'GET':
        messages.error(request, 'You must first login!')

    if request.method == 'POST':
        user = authenticate(
            request, 
            email = request.POST.get('email'), 
            password = request.POST.get('password')
        )

        if user is not None:
            if user.validated:
                handle_login(request, user)
                return redirect('dashboard')
            else:
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                activation_url = reverse('sign_up_resend', args = [uidb64])
                message = (
                    'Your account is inactive. Please, check your email or '
                    f'<a href="{activation_url}">request a new activation email</a>.'
                )
                messages.error(request, mark_safe(message)) 
        else:
            messages.error(request, 'Invalid email or password.')

    return redirect('home')

def user_logout(request):
    user = request.user

    if user.is_authenticated:
        logout(request)

    return redirect('home') 