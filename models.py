from django.db import models

class user_login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    typeuser = models.CharField(max_length=2)

    # Add more fields as per your requirements