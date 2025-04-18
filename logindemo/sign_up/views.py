from django.shortcuts import render, redirect
from .forms import CustomUserForm

def sign_up(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomUserForm()
    
    return render(
        request, 
        'sign_up/index.html', 
        { 'form': form }
    )

def home(request):
    return render(request, 'landing/home.html')