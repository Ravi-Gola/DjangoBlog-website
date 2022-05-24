from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.
class Contact(models.Model):
    sno=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.IntegerField()
    message=models.TextField()
    def __str__(self):
        return "message from" + self.name +"-"+self.email

class Post(models.Model):
    sno=models.AutoField(primary_key=True)
    category=models.CharField(max_length=50)
    title=models.CharField(max_length=150)
    content=models.TextField()
    slug=models.CharField(max_length=130)
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Blogcomment(models.Model):
    sno=models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    timezone=models.DateTimeField(default=now)
    def __str__(self):
        return self.comment
