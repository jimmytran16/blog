from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length =30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=40)
    password = models.CharField(max_length=255)
    salt = models.CharField(max_length=60)
    profile = models.ImageField(default=None,blank=True)

    def __str__(self):
        return f'Email: {self.email} Name: {self.first_name},{self.last_name}'

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField()
    subject = models.CharField(max_length=255,default=None)
    display_text = models.CharField(max_length=40)
    user_id = models.IntegerField()
    user_email = models.EmailField()
    date = models.DateTimeField(default=timezone.now)
    img = models.ImageField(upload_to="posts/",blank=True)

    def __str__(self):
        return f'{self.subject} -- {self.description}'
