import random

from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    avatar_link = models.URLField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    status = models.BooleanField(default=False)
    jwt_token = models.TextField(blank=True, null=True)
    verification_code = models.CharField(max_length=4, blank=True, null=True)
    attempts = models.IntegerField(default=3)

    def generate_verification_code(self):
        self.verification_code = f"{random.randint(1000, 9999)}"
        self.attempts = 3
        self.save()

    def __str__(self):
        return f"{self.name} {self.last_name}"


class VerificationCode(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="verification_code_relation"  # Custom related_name
    )
    code = models.CharField(max_length=6)
    expiration_time = models.DateTimeField()

    def __str__(self):
        return f"Verification code for {self.user.email}: {self.code}"
