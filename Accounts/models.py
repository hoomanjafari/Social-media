from django.db import models
from django.contrib.auth.models import User


class UserProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_related')
    age = models.PositiveIntegerField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)


class UserPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_user_related')
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} {self.body[:20]} {self.created} {self.updated}'

    def like_counter(self):
        return self.post_liked_related.count()


class PostComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment_related')
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='post_comment_related')
    replay = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replay_comment_related', null=True, blank=True)
    is_replay = models.BooleanField(default=False)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.body}'
