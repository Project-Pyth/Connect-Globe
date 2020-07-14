# Create your models here.
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now




class Post(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    body = models.TextField(max_length=10000, blank=False, null=False)
    date_posted = models.DateTimeField(default=datetime.now)
    author = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title


class Contact(models.Model):
    contact_first = models.CharField(max_length=225)
    contact_last = models.CharField(max_length=225)
    contact_email = models.CharField(max_length=225)
    contact_subject = models.CharField(max_length=225)
    contact_feedback = models.CharField(max_length=225)



class Job(models.Model):
    job_name = models.CharField(max_length=225)
    job_email = models.CharField(max_length=225)
    job_country = models.CharField(max_length=225)
    job_contact = models.BigIntegerField(default=0)
    job_tech = models.CharField(max_length=225)
    job_exp = models.IntegerField(default=0)
    job_company = models.CharField(max_length=225)
    job_qual = models.CharField(max_length=225)
    job_resume = models.FileField(upload_to='resume',null=True)

    def __str__(self):
        return self.job_name

class UProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    email = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pics',null=True, default='default.jpg')
    dob = models.DateTimeField(null=True)
    desc = models.CharField(max_length=225)
    city = models.CharField(max_length=225)



class PostComment(models.Model):
    objects = models.Manager()
    sno = models.AutoField(primary_key=True)
    comment = models.TextField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='replies')
    timestamp = models.DateTimeField(default=now)



