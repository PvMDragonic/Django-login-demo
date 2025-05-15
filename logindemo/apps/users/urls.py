from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path(
        'sign_up/', 
        views.sign_up, 
        name = 'sign_up'
    ),

    path(
        'sign_up/completed', 
        views.sign_up_completed, 
        name = 'sign_up_completed'
    ),

    path('password_change/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name = 'password_change/form.html',
        success_url = '/password_change/completed'
    ), name = 'password_change_form'),

    path('password_change/completed', auth_views.PasswordResetCompleteView.as_view(
        template_name = 'password_change/completed.html'
    ), name = 'password_change_completed')
]