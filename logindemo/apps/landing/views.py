from django.contrib.auth import authenticate, logout
from django.shortcuts import render, redirect
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

        if user is not None and user.is_active:
            handle_login(request, user)
            return redirect('dashboard') 
        else:
            messages.error(request, 'Invalid email or password.')

    return redirect('home')

def user_logout(request):
    user = request.user

    if user.is_authenticated:
        logout(request)

    return redirect('home') 