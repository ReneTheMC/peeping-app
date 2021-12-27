from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.urls import reverse

class Post(models.Model):
    image = models.ImageField(upload_to='posts')
    caption = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200)

    def get_absolute_url(self):
        return reverse('posts:post_detail',
                       args=[self.created.year, self.created.month, self.created.day, self.slug])

    def likes_counter(self):
        return self.votes.count()

    def user_can_like(self, user):
        user_like = user.votes.all()
        query_str = user_like.filter(post=self)
        if query_str.exists():
            return False
        return True


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='votes')