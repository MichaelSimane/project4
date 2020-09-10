from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    posts = models.CharField(max_length=260)
    time = models.DateTimeField(auto_now_add=False)
    like = models.ManyToManyField(User, blank=True, related_name="liked")

    def __str__(self):
        return f"{self.id} {self.user} {self.posts} {self.time} {self.like}"

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, blank=True, related_name="follower_user")
    following = models.ManyToManyField(User, blank=True, related_name="following_user")

    def __str__(self):
        return f"{self.id} {self.user} {self.followers} {self.following}"
