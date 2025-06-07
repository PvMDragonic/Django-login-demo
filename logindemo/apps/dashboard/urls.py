from django.urls import path

from users.views import acc_deletion
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_start, name = 'dashboard'),
    path('deletion/', acc_deletion, name = 'acc_deletion')
]