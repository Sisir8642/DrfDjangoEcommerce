from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ROLE = (
        ('admin', 'Admin'),
        ('customer', 'Customer')
    )

    role = models.name = models.CharField(max_length=10, choices= ROLE, default='customer')

    def __str__(self):
        return f"{self.username} ({self.role})"
    
