from django.db import models

class CustomUser(models.Model):
    username = models.CharField(max_length = 150, unique = True)
    password = models.CharField(max_length = 128)
    email = models.EmailField(unique = True)
    signup_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"