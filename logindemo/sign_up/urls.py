from django.urls import path
from . import views

urlpatterns = [
    path('sign_up/', views.sign_up, name = 'sign_up'),
    path('sign_up/success', views.successful_registration, name='successful_registration')
]