from django.contrib.auth import views as auth_views
from django.urls import path

from dashboard.views import dashboard_start
from . import views

urlpatterns = [
    path(
        'sign_up/', 
        views.sign_up_form, 
        name = 'sign_up'
    ),

    path(
        'sign_up/completed', 
        views.sign_up_completed, 
        name = 'sign_up_completed'
    ),

    path(
        'sign_up/resend/<uidb64>', 
        views.sign_up_resend, 
        name = 'sign_up_resend'
    ),

    path(
        'sign_up/activate/<uidb64>/<token>', 
        views.sign_up_activate, 
        name = 'sign_up_activate'
    ),

    path(
        'sign_up/activated', 
        views.sign_up_activate_success, 
        name = 'sign_up_activated'
    ),

    path(
        'sign_up/invalid',
        views.sign_up_activate_invalid,
        name = 'sign_up_invalid'
    ),

    path(
        'dashboard/', 
        dashboard_start, 
        name = 'dashboard'
    ),

    path('password_change/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name = 'password_change/form.html',
        success_url = '/password_change/completed'
    ), name = 'password_change_form'),

    path('password_change/completed', auth_views.PasswordResetCompleteView.as_view(
        template_name = 'password_change/completed.html'
    ), name = 'password_change_completed'),

    path(
        'deletion/email_sent', 
        views.acc_deletion_email, 
        name = 'deletion_email'
    ),

    path(
        'deletion/<uidb64>/<token>', 
        views.acc_deletion_completed, 
        name = 'acc_deletion_completed'
    )
]