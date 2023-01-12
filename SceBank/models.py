from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django import forms
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.TextField()

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='bictures')
    url = models.URLField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



class addstudent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    s_id = models.IntegerField(null=True)
    first_name = models.CharField(max_length=25, null=True)
    last_name = models.CharField(max_length=25, null=True)
    password1 = models.CharField(max_length=25, null=True)
    password2 = models.CharField(max_length=25, null=True)
    email = models.CharField(max_length=50, null=True)
    college = models.CharField(max_length=25, null=True)
    avg = models.IntegerField(null=True)


class courses(models.Model):
    course_name = models.CharField(max_length=25, null=True)
    course_price = models.IntegerField(blank=True, null=True)
    course_descripe = models.CharField(max_length=255, null=True)
    comment = forms.CharField()



class ContactUsModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=500)

    def _str_(self):
        return self.email


class ContactAdmin(models.Model):
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=500)

    def _str_(self):  # func to see email inthe tasks list
        return self.subject

class AdminMessage(models.Model):
    messageTitle = models.TextField(default="")
    messageContent = models.TextField(default="")

    def __str__(self):
        return self.messageTitle

class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    user = models.OneToOneField(User,on_delete=models.CASCADE)



class Scholarship(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    Location = models.CharField(max_length=100)
    requirements = models.CharField(max_length=250)
    Amount = models.CharField(max_length=50)
    Hours = models.CharField(max_length=50)
    image = models.ImageField(upload_to="scholarship/images")

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(Scholarship, self).delete(*args, **kwargs)
        storage.delete(path)

    def __str__(self):
        return self.title


class SmmaryDataBank(models.Model):
    name = models.CharField(verbose_name='Subject name', max_length=10, default="unknow")
    file = models.FileField(verbose_name='summary files', upload_to='bictures')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

