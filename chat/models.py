from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Contact(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user")
    last_login = models.DateTimeField(blank=True, null=True, editable=True)
    status = models.CharField(max_length=255, default='inactive')
    profile_img = models.CharField(
        max_length=255, default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png')

    def __str__(self):
        return self.user.username


class Post(models.Model):
    author = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name='author')
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.user.username


class Chat(models.Model):
    chatters = models.ManyToManyField(
        Contact, blank=True, related_name="chats")
    posts = models.ManyToManyField(Post, blank=True)

    def __str__(self):
        return "{}".format(self.pk)
