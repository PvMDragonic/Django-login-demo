from django.apps import AppConfig

class SignUpConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Registered Users'