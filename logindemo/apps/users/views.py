from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

from config.utils import handle_login
from users.models import CustomUser
from .forms import CustomUserForm

def sign_up_form(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)

        if form.is_valid():
            try:
                user = form.save()
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

def sign_up_activate(request, uidb64, token):
    invalid_reason = None
    uid = None
    user = None

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk = uid)
    except (CustomUser.DoesNotExist, ValueError, OverflowError, TypeError):
        invalid_reason = 'invalid_user'
    
    if not invalid_reason:
        if user.validated:
            invalid_reason = 'already_activated'
        elif not default_token_generator.check_token(user, token):
            invalid_reason = 'expired'

    if invalid_reason:
        request.session['activation_error'] = {
            'reason': invalid_reason,
            'uid': uidb64,
            'email': user.email if user else None
        }

        return redirect('sign_up_invalid')

    user.validated = True
    user.save()

    handle_login(request, user)

    return redirect('sign_up_activated')

def sign_up_activate_invalid(request):
    activation_error = request.session.get('activation_error')

    return render(request, 'sign_up/invalid.html', {
        'reason': activation_error['reason'],
        'uid': activation_error['uid'],
        'email': activation_error['email']
    })

@login_required
def sign_up_activate_success(request):
    return render(request, 'sign_up/activated.html', { 
        'user_name': request.user.username 
    })
    
def sign_up_resend(request, uidb64):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (CustomUser.DoesNotExist, ValueError, OverflowError, TypeError):
        user = None

    if user is not None and not user.validated:
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

@login_required
def acc_deletion(request):
    return render(request, 'acc_delete/request.html')

@login_required
def acc_deletion_email(request):
    user = request.user
    message = render_to_string('acc_delete/email.html', {
        'user': user,
        'protocol': 'https' if request.is_secure() else 'http',
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user)
    })

    send_mail(
        'Confirm Your Account Deletion', 
        message, 
        settings.DEFAULT_FROM_EMAIL, 
        [user.email]
    )

    return render(request, 'acc_delete/email_sent.html')

@login_required
def acc_deletion_completed(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk = uid)
    except (CustomUser.DoesNotExist, ValueError, OverflowError, TypeError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = False
        user.save()

        return render(request, 'acc_delete/completed.html', {
            'username': user.username
        })
    else:
        return render(request, 'acc_delete/invalid.html')