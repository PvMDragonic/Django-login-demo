from django.shortcuts import render, redirect
from .forms import CustomUserForm

def sign_up(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            request.session['user_id'] = user.id
            request.session['user_name'] = user.username

            return redirect('sign_up_completed')
    else:
        form = CustomUserForm()
    
    return render(
        request, 
        'sign_up/form.html', 
        { 'form': form }
    )

def sign_up_completed(request):
    user_name = request.session.get('user_name', 'Guest')
    return render(
        request, 
        'sign_up/successful.html', 
        { 'user_name': user_name }
    )