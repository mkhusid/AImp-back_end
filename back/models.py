from django.db import models
from django.contrib.auth.models import User, UserManager

class SUser(User):
    """User with app settings."""

    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

    def __str__(self):
        return self.username

class Audio(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(SUser)
    url = models.CharField(max_length=100)
    objects = models.Manager
    def __str__(self):
        return self.title