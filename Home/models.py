from django.db import models
from django.contrib.auth.models import User
from Accounts.models import  UserPost


class FollowUser(models.Model):
    user_is_follow = models.ForeignKey(User, on_delete=models.CASCADE, related_name='is_follow_related')
    user_is_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='is_followed_related')

    def __str__(self):
        return f'{self.user_is_follow} is following {self.user_is_followed}'


class PostLike(models.Model):
    user_liked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_liked_related')
    post_liked = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='post_liked_related')

    def __str__(self):
        return f'{self.user_liked} Liked ( {self.post_liked.body[:20]} . . . )'
