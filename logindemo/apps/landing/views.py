from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def home(request):
    return render(request, 'landing/home.html')

def dashboard_login(request):
    if request.method == 'POST':
        user = authenticate(
            request, 
            email = request.POST.get('email'), 
            password = request.POST.get('password')
        )

        if user is not None and user.is_active:
            login(request, user)
            return redirect('dashboard') 
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'landing/home.html')