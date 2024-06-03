from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    defaultCounty = models.CharField(max_length=10, default='臺中市')
    avatar = models.ImageField(
        upload_to='avatar/', default='avatar/default.jpg', null=False, blank=False)
