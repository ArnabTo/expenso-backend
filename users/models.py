from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extended user model with email as the primary identifier."""
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    currency = models.CharField(max_length=10, default='BDT')
    bank_balance = models.DecimalField(
        max_digits=15, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email
