from django.db import models
from django.utils import timezone
import datetime


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=20)
    id = models.IntegerField(primary_key=True)


class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    body = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE)  # 默认关联到User的主键


class Comment(models.Model):
    id = models.IntegerField(primary_key=True)
    body = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE)  # 发表评论的作者
    post = models.ForeignKey('Post', on_delete=models.CASCADE)  # 被评论的是哪一个post


class Follow(models.Model):
    follower=models.ForeignKey('User',on_delete=models.CASCADE,related_name='follow_follower')
    followed=models.ForeignKey('User',on_delete=models.CASCADE,auto_created='follow_followed')

