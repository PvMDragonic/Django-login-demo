from django.urls import path
from django.contrib.auth import views as auth_views
from users.forms import CustomPasswordResetForm

from dashboard.views import dashboard_start
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),

    path('login/', views.dashboard_login, name = 'login'),

    path('logout/', views.user_logout, name = 'logout'),

    path('dashboard/', dashboard_start, name = 'dashboard'),
    
    path('password_change/', auth_views.PasswordResetView.as_view(
        form_class = CustomPasswordResetForm,
        template_name = 'password_change/request.html',
        email_template_name = 'password_change/email.html',
        success_url = '/password_change/email_sent'
    ), name = 'password_change'),

    path('password_change/email_sent', auth_views.PasswordResetDoneView.as_view(
        template_name = 'password_change/email_sent.html'
    ), name = 'password_reset_sent')
]