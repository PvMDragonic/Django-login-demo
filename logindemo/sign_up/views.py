from django.shortcuts import render, redirect
from .forms import CustomUserForm

def sign_up(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name

            return redirect('successful_registration')
    else:
        form = CustomUserForm()
    
    return render(
        request, 
        'sign_up/index.html', 
        { 'form': form }
    )

def successful_registration(request):
    return render(request, 'successful_registration/index.html')