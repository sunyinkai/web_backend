from django.db import models
from django.utils import timezone
import datetime


# Create your models here.
# class Comment(models.Model):
#     id=models.IntegerField(primary_key=True)
#     body=models.TextField()
#     timestamp=models.DateTimeField(db_index=True,default=timezone.now)
#     author_id=models.IntegerField()

# class Debug(models.Model):
#     name=models.CharField(max_length=10)

class User(models.Model):
    username = models.CharField(max_length=20)
    id = models.IntegerField(primary_key=True)


class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    body = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE)  # 默认关联到User的主键
