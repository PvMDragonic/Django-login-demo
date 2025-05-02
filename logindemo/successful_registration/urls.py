from django.urls import path
from . import views

urlpatterns = [
    path('sign_up/success', views.successful_registration, name = 'successful_registration')
]