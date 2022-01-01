from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    image = models.ImageField(upload_to='posts')
    caption = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    likes=models.ManyToManyField(User,blank=True, related_name='likes')

    @property
    def total_likes(self):
        return self.likes.count() 

