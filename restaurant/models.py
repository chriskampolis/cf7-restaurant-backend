from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')

    def is_manager(self):
        return self.role == 'manager'

class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # availability = models.BooleanField(default=True)                  # FIX !!!!!!

    def __str__(self):
        return self.name

# class Reservation(models.Model):
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     seat_count = models.IntegerField()
#     reservation_time = models.DateField(auto_now=True)


    