from django.db import models

# Create your models here.
class YsArticle(models.Model):
    title = models.CharField(max_length= 100)
    author = models.CharField(max_length= 20)
    article = models.TextField(default = '')
    articletime = models.CharField(max_length=30, default='')
    createtime = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=255, default='')
    cover = models.CharField(max_length=100, default='')
    source = models.SmallIntegerField(default=0)
    category = models.CharField(max_length=10, default='')
    key = models.CharField(max_length=10, default='')
    readtimes = models.SmallIntegerField(default=0)
    reserve = models.CharField(max_length=100, default='')

class Ips(models.Model):
    ip = models.CharField(max_length=25, default='')
    t_use = models.CharField(max_length=20, default='')

class Logs(models.Model):
    log = models.CharField(max_length=255, default='')
    createtime = models.DateTimeField(auto_now=True)

class UserMain(models.Model):
    username = models.CharField(max_length = 50)
    password = models.CharField(max_length = 50)
    date = models.DateTimeField()