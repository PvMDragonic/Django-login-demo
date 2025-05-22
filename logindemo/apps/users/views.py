from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

from users.models import CustomUser
from .forms import CustomUserForm

def sign_up_form(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)

        if form.is_valid():
            try:
                user = form.save()
                user.is_active = False
                user.save()

                request.session['user_name'] = user.username
                request.session['email'] = user.email

                message = render_to_string('sign_up/email.html', {
                    'user': user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user)
                })

                send_mail(
                    'Activate Your Account', 
                    message, 
                    settings.DEFAULT_FROM_EMAIL, 
                    [user.email]
                )

                return redirect('sign_up_completed')
            except():
                pass
    else:
        form = CustomUserForm()
    
    return render(
        request, 
        'sign_up/form.html', 
        { 'form': form }
    )

def sign_up_completed(request):
    return render(request, 'sign_up/completed.html', { 
        'user_name': request.session.get('user_name', 'Guest'),
        'user_email': request.session.get('email', 'unknown@email.com') 
    })

def sign_up_activated(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk = uid)
    except (CustomUser.DoesNotExist, ValueError, OverflowError, TypeError):
        user = None

    if user is None:
        return render(request, 'sign_up/invalid.html', {
            'reason': 'invalid_user'
        })
    
    if user.is_active:
        return render(request, 'sign_up/invalid.html', {
            'reason': 'already_activated'
        })

    if not default_token_generator.check_token(user, token):
        return render(request, 'sign_up/invalid.html', { 
            'reason': 'expired',
            'uid': uidb64,
            'email': user.email 
        })

    user.is_active = True
    user.save()

    login(request, user)

    return render(request, 'sign_up/activated.html', { 
        'user_name': user.username 
    })
    
def sign_up_resend(request, uidb64):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (CustomUser.DoesNotExist, ValueError, OverflowError, TypeError):
        user = None

    if user is not None and not user.is_active:
        message = render_to_string('sign_up/email.html', {
            'user': user,
            'uid': uidb64,
            'token': default_token_generator.make_token(user),
            'domain': get_current_site(request).domain,
        })

        send_mail(
            'Activate your account',
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )

    return render(request, 'sign_up/resend.html')
