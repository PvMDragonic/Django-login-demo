from django.shortcuts import render

def successful_registration(request):
    user_name = request.session.get('user_name', 'Guest')
    return render(
        request, 
        'successful_registration/index.html', 
        { 'user_name': user_name }
    )