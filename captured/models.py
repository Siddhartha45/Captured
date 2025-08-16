import os
from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField

User = get_user_model()

def user_directory_path(instance, filename):
    return f'images/user_{instance.user.id}/{filename}'

class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photo')
    image = CloudinaryField('image')
    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
