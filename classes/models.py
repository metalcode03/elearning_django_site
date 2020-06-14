from django.db import models
from django.urls import reverse

from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from accounts.models import School, User, Profile, Student, Teacher
# Create your models here.


class  Class(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    description = models.TextField()
    # allowed_memberships = models.ManyToManyField(Membership)

    def __str__(self):
        return self.title


class Subject(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(School, on_delete=models.CASCADE)
    classes = models.ForeignKey("Class", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    # @property
    # def lessons(self):
    #     return self.lesson_set.all().order_by('outline')


class Lesson(models.Model):
    slug=models.SlugField()
    title = models.CharField(max_length=120)
    outline = models.IntegerField()
    video_url = models.CharField(max_length=129)
    subjects = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )
    thumbnail = models.ImageField(upload_to='lessons')


    def __str__(self):
        return self.title
    