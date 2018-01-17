from django.db import models
from givvy.models import User


class Contact(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)
