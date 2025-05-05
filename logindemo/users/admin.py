from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'signup_date') 
    readonly_fields = ('signup_date',)

admin.site.register(CustomUser, CustomUserAdmin)