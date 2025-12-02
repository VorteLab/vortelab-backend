from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    name = models.CharField(max_length=150, blank=True)  # 👈 mai sigur să fie optional
    company = models.CharField(max_length=150, blank=True, null=True)
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.99")
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email or self.user.username} Profile"
